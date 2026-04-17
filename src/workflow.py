"""
IT Ticket Management Workflow

Orchestrates the multi-agent workflow for processing IT support tickets
from initial analysis through risk assessment to final routing and action.
"""

import json
import logging
from typing import Optional
from datetime import datetime
from src.agents import (
    TicketAnalyzerAgent,
    RiskAssessmentAgent,
    RoutingAgent,
    create_agents
)

# Configure logging
logger = logging.getLogger(__name__)


class TicketProcessingWorkflow:
    """
    Multi-agent workflow for processing IT support tickets.
    
    Workflow steps:
    1. Analyze ticket against policies (TicketAnalyzerAgent)
    2. Assess risk level (RiskAssessmentAgent)
    3. Route and execute action (RoutingAgent)
    """
    
    def __init__(
        self,
        analyzer: TicketAnalyzerAgent,
        risk_assessor: RiskAssessmentAgent,
        router: RoutingAgent
    ):
        self.analyzer = analyzer
        self.risk_assessor = risk_assessor
        self.router = router
    
    async def process_ticket(self, ticket_data: dict) -> dict:
        """
        Process a ticket through the complete workflow.
        
        Args:
            ticket_data: Ticket information dictionary
            
        Returns:
            Complete processing results including routing decision
        """
        # Validate input
        if not ticket_data or not isinstance(ticket_data, dict):
            return {
                "status": "error",
                "error": "Invalid ticket data - must be a non-empty dictionary",
                "timestamp": datetime.now().isoformat()
            }
        
        # Ensure required fields exist
        if not ticket_data.get("ticket_id"):
            ticket_data["ticket_id"] = f"TKT-{int(datetime.now().timestamp())}"
        
        ticket_id = ticket_data.get("ticket_id", "UNKNOWN")
        logger.info(f"Starting workflow for ticket {ticket_id}")
        
        result = {
            "ticket_id": ticket_id,
            "timestamp": datetime.now().isoformat(),
            "status": "processing",
            "stages": {}
        }
        
        try:
            # Stage 1: Analyze ticket
            logger.info(f"Stage 1: Analyzing ticket {ticket_id}")
            analysis = await self.analyzer.analyze_ticket(ticket_data)
            
            # Extract analysis content and identified policies
            analysis_content = analysis.get("content") if isinstance(analysis, dict) else analysis
            identified_policies = analysis.get("policy_ids", []) if isinstance(analysis, dict) else []
            full_policies = analysis.get("identified_policies", []) if isinstance(analysis, dict) else []
            
            result["stages"]["analysis"] = {
                "status": "completed",
                "content": analysis_content,
                "identified_policies": identified_policies,
                "identified_policies_full": full_policies
            }
            logger.info(f"Stage 1 completed for ticket {ticket_id} - Identified {len(identified_policies)} policies")
            
            # Stage 2: Assess risk
            logger.info(f"Stage 2: Assessing risk for ticket {ticket_id}")
            risk_assessment = await self.risk_assessor.assess_risk(
                ticket_data,
                analysis_content
            )
            
            # Build risk calculation breakdown
            risk_calculation = {
                "base_severity": ticket_data.get('severity_reported', 'medium').upper(),
                "affected_systems_count": len(ticket_data.get('affected_systems', [])),
                "affected_systems": ticket_data.get('affected_systems', []),
                "policies_affected_count": len(identified_policies),
                "policies_affected": identified_policies,
                "policies_details": full_policies,
                "has_critical_keywords": any(kw in str(ticket_data).lower() for kw in ['malware', 'breach', 'security', 'data exposure', 'unauthorized']),
                "risk_score": risk_assessment.get("risk_score"),
                "risk_level": risk_assessment.get("risk_level")
            }
            
            result["stages"]["risk_assessment"] = {
                "status": "completed",
                "risk_score": risk_assessment.get("risk_score"),
                "risk_level": risk_assessment.get("risk_level"),
                "classification": risk_assessment.get("classification"),
                "reasoning": risk_assessment.get("reasoning"),
                "calculation_breakdown": risk_calculation
            }
            logger.info(
                f"Stage 2 completed: Risk Level {risk_assessment.get('risk_level')} "
                f"(Score: {risk_assessment.get('risk_score')})"
            )
            
            # Stage 3: Route and act
            logger.info(f"Stage 3: Routing ticket {ticket_id}")
            routing_decision = await self.router.route_and_act(
                ticket_data,
                risk_assessment
            )
            result["stages"]["routing"] = {
                "status": "completed",
                "decision": routing_decision
            }
            logger.info(f"Stage 3 completed for ticket {ticket_id}")
            
            # Final result
            result["status"] = "completed"
            result["final_action"] = {
                "risk_level": risk_assessment.get("risk_level"),
                "classification": risk_assessment.get("classification"),
                "routing": routing_decision
            }
            
        except Exception as e:
            logger.error(f"Error processing ticket {ticket_id}: {str(e)}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    async def process_batch(self, tickets: list[dict]) -> list[dict]:
        """
        Process multiple tickets.
        
        Args:
            tickets: List of ticket dictionaries
            
        Returns:
            List of processing results
        """
        results = []
        for ticket in tickets:
            result = await self.process_ticket(ticket)
            results.append(result)
        return results


async def create_workflow() -> TicketProcessingWorkflow:
    """
    Create and initialize the complete workflow.
    
    Returns:
        Initialized TicketProcessingWorkflow instance
    """
    # Create agents
    analyzer, risk_assessor, router = await create_agents()
    
    # Create workflow
    workflow = TicketProcessingWorkflow(analyzer, risk_assessor, router)
    
    return workflow


def format_workflow_result(result: dict) -> str:
    """
    Format workflow result for display.
    
    Args:
        result: Workflow result dictionary
        
    Returns:
        Formatted string representation
    """
    output = []
    output.append("\n" + "=" * 80)
    output.append(f"TICKET PROCESSING RESULT: {result.get('ticket_id')}")
    output.append("=" * 80)
    output.append(f"Status: {result.get('status')}")
    output.append(f"Timestamp: {result.get('timestamp')}")
    
    if "error" in result:
        output.append(f"\nERROR: {result['error']}")
        return "\n".join(output)
    
    # Analysis stage
    if "analysis" in result.get("stages", {}):
        output.append("\n--- STAGE 1: POLICY ANALYSIS ---")
        analysis = result["stages"]["analysis"]["content"]
        # Truncate long analysis for display
        if len(str(analysis)) > 500:
            output.append(str(analysis)[:500] + "...")
        else:
            output.append(str(analysis))
    
    # Risk assessment stage
    if "risk_assessment" in result.get("stages", {}):
        output.append("\n--- STAGE 2: RISK ASSESSMENT ---")
        risk = result["stages"]["risk_assessment"]
        output.append(f"Risk Level: {risk.get('risk_level')}")
        output.append(f"Risk Score: {risk.get('risk_score')}/100")
        output.append(f"Classification: {risk.get('classification')}")
        output.append(f"Reasoning: {risk.get('reasoning')}")
    
    # Routing stage
    if "routing" in result.get("stages", {}):
        output.append("\n--- STAGE 3: ROUTING DECISION ---")
        routing = result["stages"]["routing"]["decision"]
        output.append(json.dumps(routing, indent=2))
    
    # Final action summary
    if "final_action" in result:
        output.append("\n--- FINAL ACTION ---")
        final = result["final_action"]
        output.append(f"Risk Level: {final.get('risk_level')}")
        output.append(f"Action Type: {final['routing'].get('automation_type') or final['routing'].get('assigned_team')}")
    
    output.append("=" * 80 + "\n")
    return "\n".join(output)
