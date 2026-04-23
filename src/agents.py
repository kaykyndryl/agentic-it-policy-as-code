"""
IT Ticket Management Agents

Multi-agent workflow for analyzing IT tickets, assessing risks, and routing them
to appropriate teams or automated remediation based on severity.

Uses OpenRouter AI (OpenAI-compatible) for agent execution.
"""

import json
import os
import logging
from typing import Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables first
load_dotenv(override=False)

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenRouter client
def get_openrouter_client() -> AsyncOpenAI:
    """Create and return OpenRouter AI client."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.io/api/v1")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    
    return AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )


class TicketAnalyzerAgent:
    """
    Analyzes incoming IT support tickets and extracts key information.
    
    Checks tickets against corporate IT policies to identify compliance issues
    and policy areas that may be impacted.
    """
    
    def __init__(self, client: AsyncOpenAI):
        self.client = client
        self.name = "TicketAnalyzerAgent"
        self.model = os.getenv("OPENROUTER_MODEL", "nemetron/nemetron-3-super")
    
    async def analyze_ticket(self, ticket_data: dict) -> dict:
        """
        Analyze a ticket against IT policies.
        
        Args:
            ticket_data: Dictionary containing ticket information
            
        Returns:
            Analysis results including policy implications and detailed assessment
        """
        from src.tools import PolicyLookupTool
        
        # Auto-identify relevant policies based on ticket content
        ticket_text = f"{ticket_data.get('title', '')} {ticket_data.get('description', '')}".lower()
        identified_policies = []
        
        # Policy identification keywords
        policy_keywords = {
            "POL-001": ["password", "reset", "credential", "authentication", "login"],
            "POL-002": ["mfa", "multi-factor", "vpn", "two-factor", "2fa", "totp"],
            "POL-003": ["data", "sensitive", "confidential", "classification", "encryption", "breach", "exposure"],
            "POL-004": ["patch", "update", "vulnerability", "critical", "security patch"],
            "POL-005": ["access", "permission", "approval", "provisioning", "deprovisioning", "role"],
            "POL-006": ["device", "mdm", "mobile", "endpoint", "laptop", "computer", "antivirus"],
            "POL-007": ["incident", "malware", "suspicious", "breach", "forensic", "investigation"],
            "POL-008": ["acceptable use", "personal use", "torrent", "streaming"]
        }
        
        for policy_id, keywords in policy_keywords.items():
            if any(kw in ticket_text for kw in keywords):
                policy = PolicyLookupTool.get_policy_by_id(policy_id)
                if policy and policy_id not in [p.get('id') for p in identified_policies]:
                    identified_policies.append(policy)
        
        # Use AI for deeper analysis
        system_prompt = """You are an IT compliance analyst. Analyze the provided ticket and:
1. Extract key information (ID, subject, affected systems, department)
2. Assess compliance risk based on the identified policies
3. Explain which policy violations or implications exist
4. Recommend risk level (Low/Medium/High) based on policy impact

Be concise and specific about policy impacts."""
        
        policies_text = "\n".join([
            f"- {p.get('id')}: {p.get('title')} - {p.get('description')}"
            for p in identified_policies
        ]) if identified_policies else "No specific policies identified"
        
        user_prompt = f"""Analyze this IT support ticket:

Ticket ID: {ticket_data.get('ticket_id', 'UNKNOWN')}
Title: {ticket_data.get('title', 'N/A')}
Description: {ticket_data.get('description', 'N/A')}
Department: {ticket_data.get('department', 'N/A')}
Affected Systems: {', '.join(ticket_data.get('affected_systems', []))}
Severity Reported: {ticket_data.get('severity_reported', 'N/A')}

Identified Policies:
{policies_text}

Provide detailed analysis of this ticket's compliance implications."""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                timeout=30.0
            )
            analysis_text = response.choices[0].message.content
            logger.debug(f"TicketAnalyzerAgent AI response: {analysis_text[:300]}")
            
            return {
                "content": analysis_text,
                "identified_policies": identified_policies,
                "policy_ids": [p.get('id') for p in identified_policies]
            }
        except Exception as e:
            logger.error(f"Error in ticket analysis: {str(e)}", exc_info=True)
            return {
                "content": f"Analysis Error: {str(e)[:200]}",
                "identified_policies": identified_policies,
                "policy_ids": [p.get('id') for p in identified_policies]
            }


class RiskAssessmentAgent:
    """
    Evaluates ticket severity and assigns risk levels.
    
    Determines risk classification (Level 1/2/3) based on:
    - System criticality
    - Compliance risk
    - Potential impact
    """
    
    def __init__(self, client: AsyncOpenAI):
        self.client = client
        self.name = "RiskAssessmentAgent"
        self.model = os.getenv("OPENROUTER_MODEL", "nemetron/nemetron-3-super")
    
    async def assess_risk(self, ticket_data: dict, analysis: str) -> dict:
        """
        Assess and classify ticket risk level + AI-recommended severity.
        
        Args:
            ticket_data: Dictionary containing ticket information
            analysis: Prior analysis from ticket analyzer
            
        Returns:
            Risk assessment with severity classification + AI severity recommendation
        """
        system_prompt = """You are a risk assessment specialist. Based on the provided ticket information:
1. Evaluate the risk score (0-100)
2. Classify severity level:
   - Level 1 (Low): Common issues with standard fixes (score < 35)
   - Level 2 (Medium): Requires specialist review (score 35-65)
   - Level 3 (High): Security/compliance risks requiring escalation (score > 65)
3. Recommend an appropriate severity for the ticket based on content:
   - low: User convenience issues, can wait
   - medium: Operational impact, needs attention today
   - high: Critical business impact, urgent
   - critical: Security/compliance risk, immediate action
4. Provide clear reasoning for your classification

Return ONLY a valid JSON object with: risk_score, risk_level, classification, reasoning, ai_recommended_severity."""
        
        user_prompt = f"""Assess the risk level for this ticket:

Ticket ID: {ticket_data.get('ticket_id')}
Title: {ticket_data.get('title')}
Description: {ticket_data.get('description')}
User-Reported Severity: {ticket_data.get('severity_reported')}
Systems: {', '.join(ticket_data.get('affected_systems', []))}
Policies: {', '.join(ticket_data.get('policy_implications', []))}
Policies Count: {len(ticket_data.get('policy_implications', []))}

Prior Analysis:
{analysis}

Based on the TITLE and DESCRIPTION content (not just user input), recommend what the actual severity should be.

Return ONLY a JSON object with these fields:
{{
  "risk_score": <0-100>,
  "risk_level": <1, 2, or 3>,
  "classification": "<description>",
  "reasoning": "<explanation>",
  "ai_recommended_severity": "<low|medium|high|critical>"
}}"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                timeout=30.0
            )
            
            response_text = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                # Extract JSON from response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                    # Ensure ai_recommended_severity is included
                    if "ai_recommended_severity" not in result:
                        result["ai_recommended_severity"] = "medium"
                    return result
            except (json.JSONDecodeError, ValueError):
                pass
            
            # Fallback to default risk assessment
            logger.warning(f"Could not parse AI response for risk assessment, using fallback")
            risk_score = ticket_data.get("risk_level", 1) * 30
            risk_level = ticket_data.get("risk_level", 1)
            return {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "classification": f"Level {risk_level} - " + ("Low Risk" if risk_level == 1 else "Medium Risk" if risk_level == 2 else "High Risk"),
                "reasoning": f"Risk assessment based on severity: {ticket_data.get('severity_reported', 'unknown')}, Affected systems: {len(ticket_data.get('affected_systems', []))} system(s), Policy implications: {len(ticket_data.get('policy_implications', []))} policy(ies)",
                "ai_recommended_severity": "medium"
            }
        except Exception as e:
            logger.error(f"Error in risk assessment: {str(e)}", exc_info=True)
            # Safe fallback
            logger.warning(f"Using emergency fallback for risk assessment")
            return {
                "risk_score": 50,
                "risk_level": 2,
                "classification": "Level 2 - Medium Risk (API Error - Fallback Mode)",
                "reasoning": f"Risk assessment encountered error: {str(e)[:100]}. Using fallback analysis.",
                "ai_recommended_severity": "medium"
            }


class RoutingAgent:
    """
    Routes tickets and executes appropriate actions.
    
    - Level 1: Provides automated remediation
    - Level 2-3: Routes to appropriate support team with escalation details
    """
    
    def __init__(self, client: AsyncOpenAI):
        self.client = client
        self.name = "RoutingAgent"
        self.model = os.getenv("OPENROUTER_MODEL", "nemetron/nemetron-3-super")
    
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
        from src.tools import PolicyLookupTool
        
        risk_level = risk_assessment.get("risk_level", 1)
        title = ticket_data.get('title', '').lower()
        description = ticket_data.get('description', '').lower()
        systems = [s.lower() for s in ticket_data.get('affected_systems', [])]
        
        if risk_level == 1:
            system_prompt = """You are an IT service automation specialist. For this Level 1 (Low Risk) ticket:
1. Identify the specific issue type
2. Provide step-by-step automated remediation
3. Include success criteria and validation steps
4. Estimate time to resolution

Return ONLY a valid JSON object with: automation_type, steps (array), estimated_time_minutes, success_criteria."""
        else:
            system_prompt = """You are an IT ticket router specializing in team assignment. For this ticket:
1. Identify the appropriate support team(s) based on issue type
2. Determine escalation requirements and urgency
3. Specify priority level
4. List required information for the handling team
5. For critical incidents, include immediate actions

Return ONLY a valid JSON object with: assigned_team, priority, escalation_required, required_info (array), and if critical: immediate_actions (array)."""
        
        user_prompt = f"""Route this {risk_assessment.get('classification')} ticket:

Ticket ID: {ticket_data.get('ticket_id')}
Title: {ticket_data.get('title')}
Department: {ticket_data.get('department')}
Reported Severity: {ticket_data.get('severity_reported')}
Risk Level: {risk_level}
Risk Score: {risk_assessment.get('risk_score')}

Affected Systems: {', '.join(ticket_data.get('affected_systems', []))}
Related Policies: {', '.join(ticket_data.get('policy_implications', []))}

Description: {ticket_data.get('description', '')}

Based on the risk level and issue type, provide routing decision in JSON format only."""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=800,
                timeout=30.0
            )
            
            response_text = response.choices[0].message.content
            logger.debug(f"RoutingAgent AI response (first 300 chars): {response_text[:300]}")
            
            # Try to parse JSON response
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    parsed = json.loads(json_str)
                    logger.info(f"Routing decision parsed successfully for risk level {risk_level}")
                    return parsed
            except (json.JSONDecodeError, ValueError) as parse_error:
                logger.warning(f"Could not parse routing AI response: {str(parse_error)}")
                pass
        except Exception as e:
            logger.error(f"Error in routing: {str(e)}", exc_info=True)
        
        # Fallback routing with comprehensive action details
        logger.info(f"Using fallback routing for risk level {risk_level}")
        if risk_level == 1:
            # Level 1: Automated remediation
            if "password" in title or "reset" in title:
                return {
                    "automation_type": "password_reset",
                    "steps": [
                        "Trigger password reset link sent to user's registered email",
                        "User clicks reset link and creates new password",
                        "Verify password meets policy requirements (12+ chars, special chars)",
                        "Wait for Active Directory sync (typically 5-15 minutes)",
                        "Confirm user can log in with new password"
                    ],
                    "estimated_time_minutes": 5,
                    "success_criteria": "User successfully logs in with new password"
                }
            else:
                return {
                    "automation_type": "standard_remediation",
                    "steps": [
                        "Analyze issue from ticket details",
                        "Execute automated fix based on issue type",
                        "Verify system/service is restored",
                        "Run validation checks",
                        "Notify user of resolution"
                    ],
                    "estimated_time_minutes": 5,
                    "success_criteria": "User can access service/system with no errors"
                }
        elif risk_level == 2:
            # Level 2: Specialist review
            if "vpn" in title or "mfa" in ' '.join(systems) or "multi-factor" in title:
                return {
                    "assigned_team": "Security Operations Center (SOC) - Identity & Access Team",
                    "priority": "high",
                    "escalation_required": False,
                    "automation_agents": ["MFA Troubleshooting Agent", "VPN Connectivity Diagnostics"],
                    "required_info": [
                        "MFA device or app used (TOTP/hardware token/Windows Hello)",
                        "Error message received during MFA challenge",
                        "Last successful VPN connection time",
                        "Recent device changes or updates",
                        "Screenshots of error messages"
                    ]
                }
            elif "access" in title or "permission" in title:
                return {
                    "assigned_team": "Identity Governance Team",
                    "priority": "medium",
                    "escalation_required": False,
                    "automation_agents": ["Access Request Validator"],
                    "required_info": [
                        "Business justification for access",
                        "Manager approval confirmation",
                        "Requested permission level and resources",
                        "Duration of access needed",
                        "Department and role information"
                    ]
                }
            else:
                return {
                    "assigned_team": "IT Support Specialist Team",
                    "priority": "high",
                    "escalation_required": False,
                    "automation_agents": ["Initial Diagnostics Agent"],
                    "required_info": [
                        "Detailed description of the issue",
                        "When the issue started",
                        "System/service affected",
                        "User's role and access level",
                        "Any error messages or screenshots"
                    ]
                }
        else:  # risk_level == 3
            # Level 3: Critical escalation
            if "malware" in title or "suspicious" in title or "breach" in title:
                return {
                    "assigned_team": "Security Operations Center (SOC) + Incident Response Team",
                    "priority": "critical",
                    "escalation_required": True,
                    "automation_agents": ["Malware Analysis Agent", "Forensic Collection Agent"],
                    "required_info": [
                        "Detailed incident description",
                        "Affected user(s) and systems",
                        "Time of incident discovery",
                        "Any suspicious activities observed",
                        "Email headers (if phishing)",
                        "File hashes or attachment details",
                        "System and application logs"
                    ],
                    "immediate_actions": [
                        "Isolate affected endpoint from network if necessary",
                        "Preserve all forensic evidence and logs",
                        "Notify Compliance and Legal teams",
                        "Begin incident investigation and documentation",
                        "Activate incident tracking ticket",
                        "Contact affected users with guidance",
                        "Scan other systems for indicators of compromise",
                        "Review email logs for phishing indicators"
                    ]
                }
            elif "data" in title or "exposure" in title:
                return {
                    "assigned_team": "Data Protection & Compliance Team + SOC",
                    "priority": "critical",
                    "escalation_required": True,
                    "automation_agents": ["Data Classification Agent", "Access Audit Agent"],
                    "required_info": [
                        "Data type and classification level",
                        "Number of affected records",
                        "Time period of exposure",
                        "Systems and storage locations involved",
                        "Access logs and who accessed the data",
                        "Scope of unauthorized access",
                        "Business impact assessment"
                    ],
                    "immediate_actions": [
                        "Restrict access to affected systems",
                        "Enable enhanced monitoring and logging",
                        "Preserve all audit trails and access records",
                        "Notify management and compliance team immediately",
                        "Begin breach impact analysis",
                        "Prepare breach notification if required by law",
                        "Engage legal counsel",
                        "Initiate forensic investigation"
                    ]
                }
            else:
                return {
                    "assigned_team": "Security Operations Center (SOC) + Management",
                    "priority": "critical",
                    "escalation_required": True,
                    "automation_agents": ["Incident Assessment Agent"],
                    "required_info": [
                        "Full incident details",
                        "Affected systems and users",
                        "Incident timeline",
                        "Business impact assessment",
                        "Relevant logs and artifacts",
                        "Current containment status"
                    ],
                    "immediate_actions": [
                        "Activate incident response plan",
                        "Establish incident command center",
                        "Notify executive leadership",
                        "Document all actions taken",
                        "Preserve evidence",
                        "Engage external resources if needed",
                        "Initiate communication plan",
                        "Begin remediation planning"
                    ]
                }


# Factory function to create agents with proper client
async def create_agents() -> tuple[TicketAnalyzerAgent, RiskAssessmentAgent, RoutingAgent]:
    """
    Create agent instances with configured OpenRouter client.
    Falls back to demo agents if OpenRouter API is unavailable.
    
    Returns:
        Tuple of (analyzer, risk_assessor, router) agents
    """
    try:
        # Try to create OpenRouter client
        client = get_openrouter_client()
        
        # Test connectivity with a simple health check
        try:
            # Try a minimal API call to verify connectivity
            import asyncio
            test_response = await asyncio.wait_for(
                client.models.list(),
                timeout=5.0
            )
            logger.info("✓ OpenRouter API is reachable - using real agents")
            return (
                TicketAnalyzerAgent(client),
                RiskAssessmentAgent(client),
                RoutingAgent(client)
            )
        except Exception as api_error:
            logger.warning(f"OpenRouter API not reachable: {type(api_error).__name__}: {str(api_error)}")
            logger.info("Falling back to demo agents for offline operation...")
            from src.demo_agents import (
                DemoTicketAnalyzerAgent,
                DemoRiskAssessmentAgent,
                DemoRoutingAgent
            )
            return (
                DemoTicketAnalyzerAgent(),
                DemoRiskAssessmentAgent(),
                DemoRoutingAgent()
            )
            
    except Exception as e:
        logger.error(f"Error creating agents: {str(e)}")
        logger.info("Using demo agents as fallback...")
        from src.demo_agents import (
            DemoTicketAnalyzerAgent,
            DemoRiskAssessmentAgent,
            DemoRoutingAgent
        )
        return (
            DemoTicketAnalyzerAgent(),
            DemoRiskAssessmentAgent(),
            DemoRoutingAgent()
        )
