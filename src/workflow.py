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

    @staticmethod
    def _severity_rank(severity: str) -> int:
        mapping = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return mapping.get((severity or "").lower(), 2)

    @staticmethod
    def _rank_to_severity(rank: int) -> str:
        reverse = {1: "low", 2: "medium", 3: "high", 4: "critical"}
        return reverse.get(rank, "medium")

    def _validate_ticket_input(self, ticket_data: dict) -> dict:
        """Validate severity consistency and auto-correct obvious mismatches.

        Generates contextual messages based on ticket type and content.
        Example: Laptop lost + low severity => escalate to CRITICAL due to data exposure risk.
        """
        title = str(ticket_data.get("title", "")).lower()
        description = str(ticket_data.get("description", "")).lower()
        combined = f"{title} {description}"
        affected_systems = ticket_data.get("affected_systems", [])

        reported = str(ticket_data.get("severity_reported", "medium")).lower()
        reported_rank = self._severity_rank(reported)
        min_required_rank = 1
        reasons: list[str] = []

        # Helper to check if any pattern is in combined text (flexible matching)
        def has_pattern(text, patterns):
            """Check if any pattern appears in text, handling word variations"""
            for pattern in patterns:
                if pattern in text:
                    return True
            return False

        # Critical security incidents - escalate to CRITICAL
        critical_keywords = [
            "ddos", "dos attack", "denial of service",
            "ransomware", "malware",
            "breach", "compromised", "unauthorized access"
        ]
        
        # Device loss/theft - HIGH to CRITICAL based on systems
        device_loss_keywords = [
            "lost", "missing", "stolen", "misplaced"
        ]
        device_types = ["laptop", "device", "computer", "workstation", "phone", "mobile"]
        
        # Determine if this is a device loss case
        is_device_loss = has_pattern(combined, device_loss_keywords) and has_pattern(combined, device_types)

        # Critical security incidents
        if has_pattern(combined, critical_keywords):
            min_required_rank = max(min_required_rank, 4)
            for keyword in critical_keywords:
                if keyword in combined:
                    if "ddos" in keyword or "dos" in keyword:
                        reasons.append("Network availability attack (DDoS) poses immediate service disruption and requires CRITICAL priority for mitigation and containment")
                    elif "ransomware" in keyword:
                        reasons.append("Ransomware infection poses critical data integrity and availability risk, and requires immediate CRITICAL response")
                    elif "malware" in keyword:
                        reasons.append("Malware infection poses security risk and requires CRITICAL priority for isolation and remediation")
                    elif "breach" in keyword or "compromised" in keyword:
                        reasons.append("Security breach indicates unauthorized access and requires immediate CRITICAL investigation and containment")
                    elif "unauthorized" in keyword:
                        reasons.append("Unauthorized access indicates security incident and requires CRITICAL priority investigation")
                    break

        # Device loss - escalate based on affected systems
        if is_device_loss:
            min_required_rank = max(min_required_rank, 3)  # Start at HIGH
            reasons.append("Device loss detected: Lost device may contain sensitive data and requires HIGH priority for inventory tracking and potential remote wipe")
            
            # Escalate to CRITICAL if critical systems would be affected
            if affected_systems and any(sys in ["Active Directory", "Email", "Database"] for sys in affected_systems):
                min_required_rank = max(min_required_rank, 4)
                reasons.append("Device loss with critical system access: Lost device has credentials/access to critical systems (Active Directory, Email, Database) - escalate to CRITICAL for immediate access revocation")

        # Multi-system impact increases severity
        if len(affected_systems) >= 3 and reported_rank < 3 and not is_device_loss:
            min_required_rank = max(min_required_rank, 3)
            affected_list = ", ".join(affected_systems)
            reasons.append(f"Multiple system impact ({affected_list}): affects more than 2 critical systems, escalating to at least HIGH priority")

        # Critical system keywords (only if not already escalated)
        critical_systems = ["active directory", "email", "database"]
        impacted_critical = [sys for sys in affected_systems if any(cs in sys.lower() for cs in critical_systems)]
        if impacted_critical and reported_rank < 3 and min_required_rank < 3 and not is_device_loss:
            min_required_rank = max(min_required_rank, 3)
            reasons.append(f"Critical infrastructure impact: {', '.join(impacted_critical)} are essential IT services requiring at least HIGH priority")

        # Authentication/security policies
        auth_keywords = ["mfa", "authentication", "2fa", "two factor"]
        if has_pattern(combined, auth_keywords):
            if reported_rank < 2:
                min_required_rank = max(min_required_rank, 2)
                reasons.append("Authentication/security policy involved: adjust to at least MEDIUM priority for access control consistency")

        validated_rank = max(reported_rank, min_required_rank)
        validated = self._rank_to_severity(validated_rank)
        adjusted = validated_rank != reported_rank

        return {
            "reported_severity": reported,
            "validated_severity": validated,
            "severity_adjusted": adjusted,
            "validation_reasons": reasons,
        }
    
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
            ticket_data["ticket_id"] = f"INC-{int(datetime.now().timestamp())}"
        
        ticket_id = ticket_data.get("ticket_id", "UNKNOWN")
        logger.info(f"Starting workflow for ticket {ticket_id}")

        input_validation = self._validate_ticket_input(ticket_data)
        original_reported_severity = input_validation["reported_severity"]
        ticket_data["severity_reported"] = input_validation["validated_severity"]
        
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
                "identified_policies_full": full_policies,
                "input_validation": input_validation,
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
                "original_reported_severity": original_reported_severity.upper(),
                "affected_systems_count": len(ticket_data.get('affected_systems', [])),
                "affected_systems": ticket_data.get('affected_systems', []),
                "policies_affected_count": len(identified_policies),
                "policies_affected": identified_policies,
                "policies_details": full_policies,
                "has_critical_keywords": any(kw in str(ticket_data).lower() for kw in ['malware', 'breach', 'security', 'data exposure', 'unauthorized']),
                "risk_score": risk_assessment.get("risk_score"),
                "risk_level": risk_assessment.get("risk_level")
            }
            
            # Build risk assessment response with scoring details
            risk_assessment_response = {
                "status": "completed",
                "risk_score": risk_assessment.get("risk_score"),
                "risk_level": risk_assessment.get("risk_level"),
                "classification": risk_assessment.get("classification"),
                "reasoning": risk_assessment.get("reasoning"),
                "calculation_breakdown": risk_calculation,
                "user_reported_severity": original_reported_severity,
                "validated_severity": ticket_data.get("severity_reported", "medium"),
                "severity_adjusted": input_validation.get("severity_adjusted", False),
                "severity_adjustment_reasons": input_validation.get("validation_reasons", []),
                "ai_recommended_severity": risk_assessment.get("ai_recommended_severity", ticket_data.get("severity_reported", "medium")),
            }
            
            # Include scoring_breakdown if provided by agent (for detailed reasoning display)
            if "scoring_breakdown" in risk_assessment:
                risk_assessment_response["scoring_breakdown"] = risk_assessment.get("scoring_breakdown")
            
            result["stages"]["risk_assessment"] = risk_assessment_response
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
