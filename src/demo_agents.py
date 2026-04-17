"""
Demo Agents - Local simulation without OpenRouter API dependency

These agents provide realistic responses based on ticket data patterns
without requiring external API calls. Perfect for demonstrations and testing.
"""

import json
import os
from datetime import datetime


class DemoTicketAnalyzerAgent:
    """Analyzes tickets using local logic without API calls."""
    
    def __init__(self):
        self.name = "TicketAnalyzerAgent"
    
    async def analyze_ticket(self, ticket_data: dict) -> str:
        """Analyze ticket based on patterns."""
        ticket_id = ticket_data.get("ticket_id", "UNKNOWN")
        title = ticket_data.get("title", "").lower()
        policies = ticket_data.get("policy_implications", [])
        
        # Pattern-based analysis
        if "password" in title:
            analysis = f"Ticket {ticket_id} involves password management. Policy POL-001 applies."
        elif "mfa" in title or "vpn" in title:
            analysis = f"Ticket {ticket_id} involves authentication/MFA. Policy POL-002 applies."
        elif "malware" in title or "suspicious" in title:
            analysis = f"Ticket {ticket_id} is a security incident. Policy POL-007 (Incident Response) applies."
        elif "data" in title or "share" in title:
            analysis = f"Ticket {ticket_id} involves data handling. Policy POL-003 (Data Classification) applies."
        elif "access" in title or "approval" in title:
            analysis = f"Ticket {ticket_id} requires access control review. Policy POL-005 applies."
        else:
            analysis = f"Ticket {ticket_id} requires standard IT support. Policies: {', '.join(policies)}"
        
        return analysis


class DemoRiskAssessmentAgent:
    """Assesses risk based on ticket patterns."""
    
    def __init__(self):
        self.name = "RiskAssessmentAgent"
    
    async def assess_risk(self, ticket_data: dict, analysis: str) -> dict:
        """Assess risk level based on ticket characteristics."""
        title = ticket_data.get("title", "").lower()
        severity = ticket_data.get("severity_reported", "medium").lower()
        affected_systems = ticket_data.get("affected_systems", [])
        policies = ticket_data.get("policy_implications", [])
        
        # Base score from severity
        severity_scores = {
            "low": 10,
            "medium": 30,
            "high": 60,
            "critical": 80
        }
        risk_score = severity_scores.get(severity, 30)
        
        # Adjust for keywords
        critical_keywords = ["malware", "breach", "security", "data exposure", "unauthorized"]
        if any(kw in title for kw in critical_keywords):
            risk_score = min(95, risk_score + 20)
        
        # Adjust for policies
        if len(policies) >= 2:
            risk_score = min(90, risk_score + 10)
        
        # Adjust for affected systems criticality
        critical_systems = ["database", "vlan", "directory", "email", "vpn"]
        if any(sys.lower() in str(affected_systems).lower() for sys in critical_systems):
            risk_score = min(85, risk_score + 5)
        
        # Determine level
        if risk_score < 35:
            risk_level = 1
            classification = "Low Risk - Automated Solution Available"
        elif risk_score < 65:
            risk_level = 2
            classification = "Medium Risk - Specialist Review Required"
        else:
            risk_level = 3
            classification = "High Risk - Escalation Required"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "classification": classification,
            "reasoning": f"Score based on severity ({severity}), keywords, and {len(policies)} policy implications"
        }


class DemoRoutingAgent:
    """Routes tickets based on risk level."""
    
    def __init__(self):
        self.name = "RoutingAgent"
    
    async def route_and_act(self, ticket_data: dict, risk_assessment: dict) -> dict:
        """Route ticket and determine action."""
        risk_level = risk_assessment.get("risk_level", 2)
        title = ticket_data.get("title", "")
        
        if risk_level == 1:
            # Automated remediation
            if "password" in title.lower():
                return {
                    "automation_type": "password_reset",
                    "steps": [
                        "Send password reset email to user",
                        "User clicks reset link",
                        "User creates new password",
                        "Verify AD sync completes",
                        "Confirm user can log in"
                    ],
                    "estimated_time_minutes": 5,
                    "success_criteria": "User successfully logs in with new password"
                }
            else:
                return {
                    "automation_type": "standard_remediation",
                    "steps": ["Execute standard troubleshooting", "Verify resolution", "Document solution"],
                    "estimated_time_minutes": 10,
                    "success_criteria": "Issue resolved"
                }
        
        elif risk_level == 2:
            # Specialist review
            if "access" in title.lower():
                return {
                    "assigned_team": "Identity Governance Team",
                    "priority": "medium",
                    "escalation_required": False,
                    "required_info": [
                        "Business justification for access",
                        "Manager approval confirmation",
                        "Requested permission level"
                    ]
                }
            elif "mfa" in title.lower() or "vpn" in title.lower():
                return {
                    "assigned_team": "Security Operations Center",
                    "priority": "high",
                    "escalation_required": False,
                    "required_info": [
                        "MFA device status",
                        "Recent authentication logs",
                        "VPN client version"
                    ]
                }
            else:
                return {
                    "assigned_team": "IT Support Team",
                    "priority": "medium",
                    "escalation_required": False,
                    "required_info": ["Full ticket details", "System access logs"]
                }
        
        else:  # Level 3 - High Risk
            if "malware" in title.lower() or "suspicious" in title.lower():
                return {
                    "assigned_team": "Security Operations Center + Incident Response",
                    "priority": "critical",
                    "escalation_required": True,
                    "required_info": [
                        "Affected user details",
                        "Email headers",
                        "Attachment hash",
                        "System forensics",
                        "Data scope analysis"
                    ],
                    "immediate_actions": [
                        "Isolate affected endpoint",
                        "Preserve forensic evidence",
                        "Notify compliance team",
                        "Begin incident investigation"
                    ]
                }
            else:
                return {
                    "assigned_team": "IT Management + Security",
                    "priority": "critical",
                    "escalation_required": True,
                    "required_info": [
                        "Complete incident details",
                        "Affected systems/data",
                        "Business impact assessment"
                    ]
                }


async def create_demo_agents() -> tuple:
    """Create demo agents for local testing."""
    return (
        DemoTicketAnalyzerAgent(),
        DemoRiskAssessmentAgent(),
        DemoRoutingAgent()
    )
