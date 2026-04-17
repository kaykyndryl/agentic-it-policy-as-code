"""
IT Ticket Management Agents

Multi-agent workflow for analyzing IT tickets, assessing risks, and routing them
to appropriate teams or automated remediation based on severity.
"""

import json
import os
from typing import Optional
from dotenv import load_dotenv
from agent_framework import Agent, Message
from agent_framework.foundry import FoundryChatClient

# Load environment variables first
load_dotenv(override=False)


class TicketAnalyzerAgent:
    """
    Analyzes incoming IT support tickets and extracts key information.
    
    Checks tickets against corporate IT policies to identify compliance issues
    and policy areas that may be impacted.
    """
    
    def __init__(self, client: FoundryChatClient):
        self.client = client
        self.name = "TicketAnalyzerAgent"
    
    async def analyze_ticket(self, ticket_data: dict) -> str:
        """
        Analyze a ticket against IT policies.
        
        Args:
            ticket_data: Dictionary containing ticket information
            
        Returns:
            Analysis results including policy implications
        """
        instructions = """You are an IT compliance analyst. Analyze the provided ticket and:
1. Extract key information (ID, subject, affected systems, department)
2. Identify which IT policies are relevant
3. Assess policy compliance risks
4. Summarize findings

Be concise and specific about policy impacts. Format output as structured analysis."""
        
        async with Agent(
            client=self.client,
            name=self.name,
            instructions=instructions
        ) as agent:
            prompt = f"""Analyze this IT support ticket:

Ticket ID: {ticket_data.get('ticket_id')}
Title: {ticket_data.get('title')}
Description: {ticket_data.get('description')}
Department: {ticket_data.get('department')}
Affected Systems: {', '.join(ticket_data.get('affected_systems', []))}
Severity Reported: {ticket_data.get('severity_reported')}

Relevant policies mentioned: {', '.join(ticket_data.get('policy_implications', []))}

Provide structured analysis of this ticket's compliance implications."""
            
            response = await agent.run(prompt)
            return str(response)


class RiskAssessmentAgent:
    """
    Evaluates ticket severity and assigns risk levels.
    
    Determines risk classification (Level 1/2/3) based on:
    - System criticality
    - Compliance risk
    - Potential impact
    """
    
    def __init__(self, client: FoundryChatClient):
        self.client = client
        self.name = "RiskAssessmentAgent"
    
    async def assess_risk(self, ticket_data: dict, analysis: str) -> dict:
        """
        Assess and classify ticket risk level.
        
        Args:
            ticket_data: Dictionary containing ticket information
            analysis: Prior analysis from ticket analyzer
            
        Returns:
            Risk assessment with severity classification
        """
        instructions = """You are a risk assessment specialist. Based on the provided ticket information:
1. Evaluate the risk score (0-100)
2. Classify severity level:
   - Level 1 (Low): Common issues with standard fixes (score < 35)
   - Level 2 (Medium): Requires specialist review (score 35-65)
   - Level 3 (High): Security/compliance risks requiring escalation (score > 65)
3. Provide clear reasoning for your classification
4. Identify approval requirements if any

Return response as JSON with: risk_score, risk_level, classification, reasoning."""
        
        async with Agent(
            client=self.client,
            name=self.name,
            instructions=instructions
        ) as agent:
            prompt = f"""Assess the risk level for this ticket:

Ticket ID: {ticket_data.get('ticket_id')}
Title: {ticket_data.get('title')}
Severity: {ticket_data.get('severity_reported')}
Systems: {', '.join(ticket_data.get('affected_systems', []))}
Policies: {', '.join(ticket_data.get('policy_implications', []))}
Policies Count: {len(ticket_data.get('policy_implications', []))}

Prior Analysis:
{analysis}

Provide risk assessment in JSON format with these fields:
- risk_score (0-100)
- risk_level (1, 2, or 3)
- classification (description)
- reasoning (explanation)"""
            
            response = await agent.run(prompt)
            
            # Try to parse JSON response
            try:
                response_text = str(response)
                # Extract JSON from response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                pass
            
            # Fallback to default risk assessment
            return {
                "risk_score": ticket_data.get("risk_level", 1) * 30,
                "risk_level": ticket_data.get("risk_level", 1),
                "classification": f"Level {ticket_data.get('risk_level', 1)} ticket",
                "reasoning": "Risk assessment based on ticket data"
            }


class RoutingAgent:
    """
    Routes tickets and executes appropriate actions.
    
    - Level 1: Provides automated remediation
    - Level 2-3: Routes to appropriate support team with escalation details
    """
    
    def __init__(self, client: FoundryChatClient):
        self.client = client
        self.name = "RoutingAgent"
    
    async def route_and_act(
        self,
        ticket_data: dict,
        risk_assessment: dict
    ) -> dict:
        """
        Route ticket and determine action based on risk level.
        
        Args:
            ticket_data: Dictionary containing ticket information
            risk_assessment: Risk assessment results
            
        Returns:
            Routing decision with assigned team/action
        """
        risk_level = risk_assessment.get("risk_level", 1)
        
        if risk_level == 1:
            instructions = """You are an IT service automation specialist. Based on the Level 1 ticket:
1. Identify common issues and standard procedures
2. Provide step-by-step automated remediation
3. Include success criteria
4. Estimate time to resolution

Return response as JSON with: automation_type, steps, estimated_time_minutes, success_criteria."""
        else:
            instructions = """You are an IT ticket router. Based on the Level 2-3 ticket:
1. Identify the appropriate support team
2. Determine escalation requirements
3. Specify priority level
4. List required information for the handling team

Return response as JSON with: assigned_team, priority, escalation_required, required_info."""
        
        async with Agent(
            client=self.client,
            name=self.name,
            instructions=instructions
        ) as agent:
            prompt = f"""Route this {risk_assessment.get('classification')} ticket:

Ticket ID: {ticket_data.get('ticket_id')}
Title: {ticket_data.get('title')}
Department: {ticket_data.get('department')}
Reported Severity: {ticket_data.get('severity_reported')}
Risk Level: {risk_level}
Risk Score: {risk_assessment.get('risk_score')}

Affected Systems: {', '.join(ticket_data.get('affected_systems', []))}
Related Policies: {', '.join(ticket_data.get('policy_implications', []))}

Provide routing decision in JSON format."""
            
            response = await agent.run(prompt)
            
            # Try to parse JSON response
            try:
                response_text = str(response)
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                pass
            
            # Fallback routing
            if risk_level == 1:
                return {
                    "automation_type": "standard_remediation",
                    "steps": ["Execute automated fix"],
                    "estimated_time_minutes": 10,
                    "success_criteria": "User regains access"
                }
            else:
                return {
                    "assigned_team": "IT Support Team",
                    "priority": "high" if risk_level == 3 else "medium",
                    "escalation_required": risk_level == 3,
                    "required_info": ["Full ticket details", "System access logs"]
                }


# Factory function to create agents with proper client
async def create_agents() -> tuple[TicketAnalyzerAgent, RiskAssessmentAgent, RoutingAgent]:
    """
    Create agent instances with configured Foundry client.
    
    Returns:
        Tuple of (analyzer, risk_assessor, router) agents
    """
    from azure.identity import DefaultAzureCredential
    
    # Get Foundry configuration
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model_deployment_name = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME")
    
    if not project_endpoint or not model_deployment_name:
        raise ValueError(
            "Missing Foundry configuration. Set FOUNDRY_PROJECT_ENDPOINT "
            "and FOUNDRY_MODEL_DEPLOYMENT_NAME in .env"
        )
    
    # Create client
    credential = DefaultAzureCredential()
    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model_deployment_name,
        credential=credential,
    )
    
    return (
        TicketAnalyzerAgent(client),
        RiskAssessmentAgent(client),
        RoutingAgent(client)
    )
