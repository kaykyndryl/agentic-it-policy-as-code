"""
IT Ticket Management Tools

This module defines all tools used by the multi-agent workflow for ticket processing,
policy lookup, risk assessment, and routing decisions.
"""

import json
from typing import Any, Optional

from src.rego_data import load_rego_data


# Initialize data from Rego files
POLICIES_DATA = load_rego_data("policies.rego", "policies", "policies")
TICKETS_DATA = load_rego_data("sample_tickets.rego", "tickets", "tickets")


class PolicyLookupTool:
    """
    Tool for searching and retrieving IT policies.
    
    Supports searching by policy ID, category, or keyword in policy content.
    """
    
    @staticmethod
    def search_by_category(category: str) -> list[dict]:
        """Search policies by category."""
        policies = POLICIES_DATA.get("policies", [])
        return [p for p in policies if p.get("category") == category]
    
    @staticmethod
    def search_by_keyword(keyword: str) -> list[dict]:
        """Search policies by keyword in title or description."""
        keyword_lower = keyword.lower()
        policies = POLICIES_DATA.get("policies", [])
        results = []
        for policy in policies:
            if (keyword_lower in policy.get("title", "").lower() or 
                keyword_lower in policy.get("description", "").lower()):
                results.append(policy)
        return results
    
    @staticmethod
    def get_policy_by_id(policy_id: str) -> Optional[dict]:
        """Retrieve a specific policy by ID."""
        policies = POLICIES_DATA.get("policies", [])
        for policy in policies:
            if policy.get("id") == policy_id:
                return policy
        return None
    
    @staticmethod
    def list_all_policies() -> list[dict]:
        """Return all available policies."""
        return POLICIES_DATA.get("policies", [])
    
    @staticmethod
    def execute(search_type: str = "keyword", query: str = "") -> str:
        """Execute the policy lookup tool."""
        if search_type == "category":
            results = PolicyLookupTool.search_by_category(query)
        elif search_type == "id":
            result = PolicyLookupTool.get_policy_by_id(query)
            results = [result] if result else []
        elif search_type == "all":
            results = PolicyLookupTool.list_all_policies()
        else:  # keyword
            results = PolicyLookupTool.search_by_keyword(query)
        
        if not results:
            return f"No policies found matching '{query}'"
        
        return json.dumps(results, indent=2)


class TicketDatabaseTool:
    """
    Tool for accessing the ticket database.
    
    Supports retrieving ticket information and tracking ticket status.
    """
    
    @staticmethod
    def get_ticket(ticket_id: str) -> Optional[dict]:
        """Retrieve a specific ticket by ID."""
        tickets = TICKETS_DATA.get("tickets", [])
        for ticket in tickets:
            if ticket.get("ticket_id") == ticket_id:
                return ticket
        return None
    
    @staticmethod
    def get_tickets_by_department(department: str) -> list[dict]:
        """Retrieve all tickets for a specific department."""
        tickets = TICKETS_DATA.get("tickets", [])
        return [t for t in tickets if t.get("department") == department]
    
    @staticmethod
    def get_all_tickets() -> list[dict]:
        """Retrieve all tickets."""
        return TICKETS_DATA.get("tickets", [])
    
    @staticmethod
    def update_ticket_status(ticket_id: str, status: str) -> bool:
        """Update ticket status (in production, this would update a database)."""
        # For this simulation, log the update
        print(f"[DB UPDATE] Ticket {ticket_id} status updated to: {status}")
        return True
    
    @staticmethod
    def execute(operation: str = "get", ticket_id: str = "", department: str = "") -> str:
        """Execute the ticket database tool."""
        if operation == "get":
            ticket = TicketDatabaseTool.get_ticket(ticket_id)
            if not ticket:
                return f"Ticket {ticket_id} not found"
            return json.dumps(ticket, indent=2)
        
        elif operation == "list_by_department":
            tickets = TicketDatabaseTool.get_tickets_by_department(department)
            return json.dumps(tickets, indent=2)
        
        elif operation == "list_all":
            tickets = TicketDatabaseTool.get_all_tickets()
            return json.dumps(tickets, indent=2)
        
        return "Unknown operation"


class RiskEvaluationTool:
    """
    Tool for evaluating ticket risk levels and severity.
    
    Assigns risk scores and severity classifications based on ticket characteristics.
    """
    
    @staticmethod
    def calculate_risk_score(ticket_data: dict) -> int:
        """
        Calculate risk score (0-100) based on ticket characteristics.
        
        Factors:
        - Policy violations
        - Affected system criticality
        - Reported severity
        - User privilege level
        """
        score = 0
        
        # Base score from reported severity
        severity_map = {"low": 10, "medium": 40, "high": 60, "critical": 85}
        score += severity_map.get(ticket_data.get("severity_reported", "low").lower(), 10)
        
        # Add points for policy implications
        policy_count = len(ticket_data.get("policy_implications", []))
        score += policy_count * 10
        
        # Add points for high-criticality systems
        critical_systems = ["Database", "VPN", "Email", "ActiveDirectory", "MFA"]
        affected_systems = ticket_data.get("affected_systems", [])
        for system in affected_systems:
            if any(crit in system for crit in critical_systems):
                score += 15
        
        # Cap at 100
        return min(score, 100)
    
    @staticmethod
    def classify_risk_level(risk_score: int) -> tuple[int, str]:
        """Classify risk score into severity levels."""
        if risk_score < 35:
            return 1, "Low Risk - Can be automated"
        elif risk_score < 65:
            return 2, "Medium Risk - Requires specialist review"
        else:
            return 3, "High Risk - Escalation required"
    
    @staticmethod
    def execute(ticket_data: dict) -> str:
        """Execute the risk evaluation tool."""
        if not ticket_data:
            return "No ticket data provided"
        
        risk_score = RiskEvaluationTool.calculate_risk_score(ticket_data)
        risk_level, classification = RiskEvaluationTool.classify_risk_level(risk_score)
        
        result = {
            "ticket_id": ticket_data.get("ticket_id"),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "classification": classification,
            "factors_analyzed": {
                "reported_severity": ticket_data.get("severity_reported"),
                "policy_violations": len(ticket_data.get("policy_implications", [])),
                "affected_systems": ticket_data.get("affected_systems", [])
            }
        }
        
        return json.dumps(result, indent=2)


class RemediationTool:
    """
    Tool for automated remediation of Level 1 tickets.
    
    Provides automated solutions for common, low-risk IT issues.
    """
    
    REMEDIATION_DATABASE = {
        "password_reset": {
            "steps": [
                "Initiate password reset through Azure AD/Active Directory",
                "User receives reset link via registered email",
                "User sets new password following policy requirements",
                "Account access restored"
            ],
            "time_to_resolve": "5-10 minutes",
            "success_rate": "99%"
        },
        "monitor_connection": {
            "steps": [
                "Check display adapter drivers are up-to-date",
                "Reseat USB/displayport connections",
                "Restart display settings in Windows",
                "If USB monitor, try different USB port",
                "Restart computer if issue persists"
            ],
            "time_to_resolve": "10-15 minutes",
            "success_rate": "95%"
        },
        "printer_driver": {
            "steps": [
                "Download latest printer driver from manufacturer",
                "Run device manager and update device driver",
                "Add printer through settings",
                "Send test print",
                "Configure as default if needed"
            ],
            "time_to_resolve": "10-20 minutes",
            "success_rate": "94%"
        },
        "password_policies": {
            "steps": [
                "Verify new password meets complexity requirements",
                "Ensure password is not in recently used list",
                "Check if account is locked due to policy",
                "Reset password and unlock account",
                "Inform user of password requirements"
            ],
            "time_to_resolve": "5 minutes",
            "success_rate": "100%"
        }
    }
    
    @staticmethod
    def suggest_remediation(ticket_title: str, issue_category: str) -> Optional[dict]:
        """Suggest automated remediation steps for a ticket."""
        # Simple keyword matching for suggestion
        title_lower = ticket_title.lower()
        
        suggestions = []
        if "password" in title_lower and "reset" in title_lower:
            suggestions.append("password_reset")
        if "monitor" in title_lower or "display" in title_lower:
            suggestions.append("monitor_connection")
        if "printer" in title_lower:
            suggestions.append("printer_driver")
        if "password" in title_lower and "policy" in title_lower:
            suggestions.append("password_policies")
        
        if suggestions:
            return RemediationTool.REMEDIATION_DATABASE.get(suggestions[0])
        return None
    
    @staticmethod
    def execute(ticket_title: str = "", issue_category: str = "") -> str:
        """Execute the remediation tool."""
        remediation = RemediationTool.suggest_remediation(ticket_title, issue_category)
        
        if not remediation:
            return "No automated remediation available for this ticket type"
        
        result = {
            "remediation_available": True,
            "estimated_time": remediation["time_to_resolve"],
            "success_rate": remediation["success_rate"],
            "steps": remediation["steps"]
        }
        
        return json.dumps(result, indent=2)


class NotificationTool:
    """
    Tool for routing tickets and notifying support teams.
    
    Handles ticket assignment and team notifications.
    """
    
    TEAM_ASSIGNMENTS = {
        "password_management": "Identity & Access Team",
        "multi_factor_authentication": "Security Operations Team",
        "data_classification": "Security & Compliance Team",
        "patch_management": "Infrastructure Team",
        "access_control": "Identity Governance Team",
        "device_management": "Endpoint Management Team",
        "incident_response": "Security Operations Center",
        "acceptable_use": "Compliance Team"
    }
    
    @staticmethod
    def get_team_for_policy(policy_id: str) -> Optional[str]:
        """Get the responsible team for a policy."""
        # Get policy category
        policies = POLICIES_DATA.get("policies", [])
        for policy in policies:
            if policy.get("id") == policy_id:
                category = policy.get("category")
                return NotificationTool.TEAM_ASSIGNMENTS.get(category)
        return None
    
    @staticmethod
    def route_ticket(ticket_id: str, risk_level: int, policies: list) -> dict:
        """Route ticket to appropriate team."""
        if risk_level == 1:
            return {
                "routing_type": "automated",
                "assigned_to": "Automated System",
                "action": "auto_remediation",
                "priority": "low"
            }
        else:
            # Find primary policy and get team
            if policies:
                team = NotificationTool.get_team_for_policy(policies[0])
            else:
                team = "General IT Support"
            
            priority = "medium" if risk_level == 2 else "critical"
            
            return {
                "routing_type": "manual",
                "assigned_to": team,
                "action": "escalate_to_team",
                "priority": priority,
                "notification_channels": ["email", "dashboard", "sms"]
            }
    
    @staticmethod
    def execute(ticket_id: str = "", risk_level: int = 1, policy_ids: list = None) -> str:
        """Execute the notification tool."""
        if policy_ids is None:
            policy_ids = []
        
        routing = NotificationTool.route_ticket(ticket_id, risk_level, policy_ids)
        
        # Log the notification (in production, would send actual notifications)
        print(f"[NOTIFICATION] Ticket {ticket_id} routed to {routing['assigned_to']}")
        print(f"[NOTIFICATION] Priority: {routing['priority']}")
        
        return json.dumps(routing, indent=2)
