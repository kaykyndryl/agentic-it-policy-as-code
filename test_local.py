"""
IT Ticket Management System - Local Testing Script

Test the workflow locally with sample data.
Uses OpenRouter AI for agent execution (requires OPENROUTER_API_KEY in .env).
"""

import json
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=False)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_sample_data():
    """Load sample tickets and policies."""
    data_dir = Path(__file__).parent / "data"
    
    with open(data_dir / "sample_tickets.json") as f:
        tickets = json.load(f)
    
    with open(data_dir / "policies.json") as f:
        policies = json.load(f)
    
    return tickets["tickets"], policies["policies"]


def print_ticket_summary(ticket: dict):
    """Print a summary of ticket information."""
    print("\n" + "=" * 60)
    print(f"TICKET: {ticket['ticket_id']} - {ticket['title']}")
    print("=" * 60)
    print(f"Department: {ticket['department']}")
    print(f"Severity: {ticket['severity_reported']}")
    print(f"Systems: {', '.join(ticket['affected_systems'])}")
    print(f"Policies: {', '.join(ticket['policy_implications']) if ticket['policy_implications'] else 'None'}")
    print(f"Expected Risk Level: {ticket.get('risk_level', 'TBD')}")
    print("-" * 60)


def print_policy_summary(policy: dict):
    """Print a summary of a policy."""
    print(f"\n📋 {policy['id']}: {policy['title']}")
    print(f"   Category: {policy['category']}")
    print(f"   Scope: {policy['compliance_level']}")
    print(f"   Key Reqs: {len(policy['key_requirements'])} requirements")


async def test_ticket_analysis():
    """Test ticket analysis with mock workflow."""
    print("\n" + "=" * 80)
    print("IT TICKET MANAGEMENT SYSTEM - LOCAL TEST")
    print("=" * 80)
    
    tickets, policies = load_sample_data()
    
    # Display available data
    print(f"\n📊 Loaded {len(tickets)} sample tickets")
    print(f"📋 Loaded {len(policies)} IT policies")
    
    # Show sample tickets
    print("\n--- SAMPLE TICKETS ---")
    for ticket in tickets[:3]:  # Show first 3
        print_ticket_summary(ticket)
    
    # Show sample policies
    print("\n--- SAMPLE POLICIES ---")
    for policy in policies[:3]:  # Show first 3
        print_policy_summary(policy)
    
    # Demonstrate tool capabilities
    print("\n" + "=" * 80)
    print("TOOL CAPABILITIES DEMONSTRATION")
    print("=" * 80)
    
    from src.tools import (
        PolicyLookupTool,
        TicketDatabaseTool,
        RiskEvaluationTool,
        RemediationTool,
        NotificationTool
    )
    
    # Test PolicyLookupTool
    print("\n1. POLICY LOOKUP TOOL")
    print("-" * 40)
    lookup_tool = PolicyLookupTool()
    mfa_policies = lookup_tool.execute(search_type="keyword", query="multi-factor")
    print(f"Policies found for 'multi-factor': {len(json.loads(mfa_policies))} policies")
    
    # Test TicketDatabaseTool
    print("\n2. TICKET DATABASE TOOL")
    print("-" * 40)
    db_tool = TicketDatabaseTool()
    ticket = db_tool.execute(operation="get", ticket_id="INC-001")
    print(f"Retrieved ticket INC-001:")
    print(f"  Title: {json.loads(ticket).get('title')}")
    print(f"  Status: {json.loads(ticket).get('status')}")
    
    # Test RiskEvaluationTool
    print("\n3. RISK EVALUATION TOOL")
    print("-" * 40)
    risk_tool = RiskEvaluationTool()
    risk = risk_tool.execute(ticket_data=tickets[0])
    risk_result = json.loads(risk)
    print(f"Risk Assessment for {tickets[0]['ticket_id']}:")
    print(f"  Risk Score: {risk_result.get('risk_score')}")
    print(f"  Risk Level: {risk_result.get('risk_level')}")
    print(f"  Classification: {risk_result.get('classification')}")
    
    # Test RemediationTool
    print("\n4. REMEDIATION TOOL")
    print("-" * 40)
    remediation_tool = RemediationTool()
    remediation = remediation_tool.execute(
        ticket_title=tickets[0]['title'],
        issue_category="common_issues"
    )
    remediation_result = json.loads(remediation)
    print(f"Remediation for '{tickets[0]['title']}':")
    if remediation_result.get('remediation_available'):
        print(f"  Available: Yes")
        print(f"  Steps: {len(remediation_result.get('steps', []))} steps")
        print(f"  Time: {remediation_result.get('estimated_time')}")
        print(f"  Success Rate: {remediation_result.get('success_rate')}")
    else:
        print(f"  Available: No automated remediation")
    
    # Test NotificationTool
    print("\n5. NOTIFICATION/ROUTING TOOL")
    print("-" * 40)
    notify_tool = NotificationTool()
    routing = notify_tool.execute(
        ticket_id=tickets[0]['ticket_id'],
        risk_level=1,
        policy_ids=tickets[0].get('policy_implications', [])
    )
    routing_result = json.loads(routing)
    print(f"Routing for {tickets[0]['ticket_id']}:")
    print(f"  Routing Type: {routing_result.get('routing_type')}")
    print(f"  Assigned To: {routing_result.get('assigned_to')}")
    print(f"  Priority: {routing_result.get('priority')}")
    
    print("\n" + "=" * 80)
    print("✅ LOCAL TEST COMPLETE")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Configure Foundry credentials in .env file")
    print("2. Run the HTTP server: python -m src.main")
    print("3. Send ticket processing requests to http://localhost:8000")
    print("4. Use VS Code debugging (F5) for interactive development")


if __name__ == "__main__":
    asyncio.run(test_ticket_analysis())
