#!/usr/bin/env python3
"""
Web Demo Test Script for IT Ticket Management System

Tests the web interface with three quick example scenarios:
1. Password Reset (Level 1 - Low Risk - Automated)
2. VPN/MFA Issue (Level 2 - Medium Risk - Specialist Review)
3. Security Alert (Level 3 - High Risk - Escalation)

Run this script to test the web interface with example tickets.
Usage: python web_demo_test.py
"""

import json
import asyncio
import sys
from pathlib import Path

# Test tickets with detailed scenarios
TEST_TICKETS = [
    {
        "name": "Password Reset",
        "scenario": "Level 1 - LOW RISK - AUTOMATED",
        "ticket": {
            "ticket_id": "INC-DEMO-001",
            "title": "Password Reset Request",
            "description": "User forgot their password and cannot log in to their work account. Tried password recovery email but it didn't arrive.",
            "department": "Finance",
            "affected_systems": ["Active Directory", "Email", "Microsoft 365"],
            "severity_reported": "high",
            "policy_implications": ["POL-001"]
        }
    },
    {
        "name": "VPN/MFA Issue",
        "scenario": "Level 2 - MEDIUM RISK - SPECIALIST REVIEW",
        "ticket": {
            "ticket_id": "INC-DEMO-002",
            "title": "Cannot Access VPN - MFA Failures",
            "description": "Employee reports repeated MFA failures when attempting to connect to corporate VPN. They are working from home and cannot access necessary customer data. They've tried on mobile phone authenticator app but keeps getting authentication timeouts.",
            "department": "Engineering",
            "affected_systems": ["VPN", "MFA", "Identity Provider"],
            "severity_reported": "critical",
            "policy_implications": ["POL-002", "POL-005"]
        }
    },
    {
        "name": "Security Alert",
        "scenario": "Level 3 - HIGH RISK - ESCALATION REQUIRED",
        "ticket": {
            "ticket_id": "INC-DEMO-003",
            "title": "Suspicious Email Download - Potential Malware Detected",
            "description": "User received suspicious email claiming to be a critical security update from 'Microsoft'. Email included an attachment 'Critical_Update.exe'. User downloaded and opened the attachment. System antivirus immediately triggered multiple alerts. User also reports seeing unusual network activity. IT department detected outbound connections to known malicious IPs.",
            "department": "Sales",
            "affected_systems": ["Endpoints", "Email", "Network", "Active Directory"],
            "severity_reported": "critical",
            "policy_implications": ["POL-003", "POL-004", "POL-006", "POL-007"]
        }
    }
]


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_ticket_json(ticket_data, name, scenario):
    """Print ticket data as JSON for copy-paste."""
    print(f"📋 {name} - {scenario}")
    print("\n```json")
    print(json.dumps(ticket_data, indent=2))
    print("```\n")
    return ticket_data


async def test_ticket_via_api(ticket_data, base_url="http://localhost:8000"):
    """Test processing a ticket via the API."""
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{base_url}/api/tickets/process",
                json=ticket_data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"❌ Error: HTTP {response.status}")
                    text = await response.text()
                    print(f"Response: {text[:200]}")
                    return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def display_results(result):
    """Display the processing results."""
    if not result:
        print("No results to display")
        return
    
    ticket_id = result.get('ticket_id', 'UNKNOWN')
    status = result.get('status', 'unknown')
    
    print(f"\n{'='*80}")
    print(f"📊 PROCESSING RESULTS FOR {ticket_id}")
    print(f"{'='*80}\n")
    
    if status == 'error':
        print(f"❌ ERROR: {result.get('error', 'Unknown error')}\n")
        return
    
    # Risk Assessment
    risk_info = result.get('stages', {}).get('risk_assessment', {})
    print(f"📈 RISK ASSESSMENT")
    print(f"  Risk Score: {risk_info.get('risk_score', 'N/A')}/100")
    print(f"  Risk Level: {risk_info.get('risk_level', 'N/A')}")
    print(f"  Classification: {risk_info.get('classification', 'N/A')}")
    print(f"  Reasoning: {risk_info.get('reasoning', 'N/A')}\n")
    
    # Calculation Breakdown
    calc = risk_info.get('calculation_breakdown', {})
    if calc:
        print(f"📋 CALCULATION BREAKDOWN")
        print(f"  Base Severity: {calc.get('base_severity', 'N/A')}")
        print(f"  Affected Systems: {calc.get('affected_systems_count', 0)} - {calc.get('affected_systems', [])}")
        print(f"  Policies Affected: {calc.get('policies_affected_count', 0)}")
        if calc.get('policies_affected'):
            for policy_id in calc.get('policies_affected', []):
                print(f"    - {policy_id}")
        print(f"  Critical Keywords: {'✓ YES' if calc.get('has_critical_keywords') else '✗ NO'}\n")
    
    # Policy Details
    if calc.get('policies_details'):
        print(f"📜 IDENTIFIED POLICIES")
        for policy in calc.get('policies_details', []):
            print(f"  {policy.get('id')} - {policy.get('title')}")
            print(f"    Category: {policy.get('category')}")
            print(f"    Description: {policy.get('description', 'N/A')}\n")
    
    # Analysis
    analysis = result.get('stages', {}).get('analysis', {})
    if analysis.get('content'):
        print(f"💭 AI ANALYSIS & REASONING")
        print(f"  {analysis.get('content', 'N/A')[:300]}...\n")
    
    # Routing Decision
    routing = result.get('stages', {}).get('routing', {}).get('decision', {})
    if routing:
        print(f"🎯 RECOMMENDED ACTIONS")
        
        if routing.get('automation_type'):
            print(f"  Automation Type: {routing.get('automation_type')}")
            print(f"  Estimated Time: {routing.get('estimated_time_minutes')} minutes")
            print(f"  Success Criteria: {routing.get('success_criteria')}")
            print(f"  Steps:")
            for i, step in enumerate(routing.get('steps', []), 1):
                print(f"    {i}. {step}")
        else:
            print(f"  Assigned Team: {routing.get('assigned_team', 'N/A')}")
            print(f"  Priority: {routing.get('priority', 'N/A').upper()}")
            print(f"  Escalation Required: {'✓ YES' if routing.get('escalation_required') else '✗ NO'}")
            if routing.get('automation_agents'):
                print(f"  Automation Agents:")
                for agent in routing.get('automation_agents', []):
                    print(f"    - {agent}")
            if routing.get('required_info'):
                print(f"  Required Information:")
                for info in routing.get('required_info', []):
                    print(f"    - {info}")
            if routing.get('immediate_actions'):
                print(f"  Immediate Actions:")
                for action in routing.get('immediate_actions', []):
                    print(f"    ⚡ {action}")
    
    print(f"\n{'='*80}\n")


def print_web_instructions():
    """Print instructions for testing via web interface."""
    print_header("🌐 WEB INTERFACE TESTING INSTRUCTIONS")
    
    print("""
1. ENSURE SERVER IS RUNNING
   Terminal command: python run_web.py
   
2. OPEN YOUR BROWSER
   Navigate to: http://localhost:8000
   
3. COPY-PASTE TEST TICKETS
   Below are three formatted JSON tickets you can copy and paste
   into the web form. Choose "Paste JSON" to submit them.
   
4. OBSERVE THE RESULTS
   - Risk Score Calculation Breakdown
   - Identified Policies with Details
   - AI Analysis & Reasoning
   - Recommended Actions (Automated or Team Assignment)
   - Automation Agents (if Level 1)
   - Escalation Details (if Level 3)

""")


def print_curl_instructions():
    """Print curl instructions for testing."""
    print_header("🔧 CURL COMMAND TESTING")
    
    print("""
Alternatively, test via command line with curl:

For each ticket below, run:
  curl -X POST http://localhost:8000/api/tickets/process \\
    -H "Content-Type: application/json" \\
    -d '<JSON_TICKET_HERE>'

Example:
  curl -X POST http://localhost:8000/api/tickets/process \\
    -H "Content-Type: application/json" \\
    -d '{
      "ticket_id": "TKT-DEMO-001",
      "title": "Password Reset Request",
      ...
    }'

""")


def main():
    """Main test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Demo test script for IT Ticket Management Web Interface"
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Test via API (requires running server)"
    )
    parser.add_argument(
        "--ticket",
        type=int,
        choices=[1, 2, 3],
        help="Test specific ticket (1=Password, 2=VPN/MFA, 3=Security)"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    print_header("🧪 IT TICKET MANAGEMENT - WEB DEMO TEST SCRIPT")
    
    print("""
This script demonstrates three common IT support scenarios:
  1️⃣  Password Reset - Level 1 (Low Risk, Automated)
  2️⃣  VPN/MFA Issue - Level 2 (Medium Risk, Specialist Review)
  3️⃣  Security Alert - Level 3 (High Risk, Escalation)

Each scenario includes policy mapping, risk scoring, and action recommendations.
""")
    
    if args.api:
        # Test via API
        print("\n🔌 TESTING VIA API\n")
        
        test_range = [args.ticket - 1] if args.ticket else range(len(TEST_TICKETS))
        
        for idx in test_range:
            test_case = TEST_TICKETS[idx]
            print(f"\n{'='*80}")
            print(f"Testing: {test_case['name']} ({test_case['scenario']})")
            print(f"{'='*80}\n")
            
            print(f"📤 Sending to {args.url}/api/tickets/process...")
            
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                test_ticket_via_api(test_case['ticket'], args.url)
            )
            
            display_results(result)
            
            if idx < len(test_range) - 1:
                input("Press Enter to continue to next ticket...")
    
    else:
        # Show instructions for manual testing
        print_web_instructions()
        
        for i, test_case in enumerate(TEST_TICKETS, 1):
            print(f"\n{'='*80}")
            print(f"TEST CASE {i}: {test_case['name']}")
            print(f"Scenario: {test_case['scenario']}")
            print(f"{'='*80}\n")
            
            print_ticket_json(test_case['ticket'], test_case['name'], test_case['scenario'])
            
            if i < len(TEST_TICKETS):
                print("\n" + "-"*80 + "\n")
        
        print_curl_instructions()
        
        print_header("📝 NEXT STEPS")
        print("""
1. Start the web server:
   python run_web.py

2. Open browser to: http://localhost:8000

3. Copy one of the JSON tickets above and paste into the web form

4. Click "Process Ticket"

5. Review the comprehensive output:
   - Risk Score Breakdown
   - Policy Analysis
   - AI Reasoning
   - Recommended Actions

To test via API instead, run:
   python web_demo_test.py --api [--ticket 1|2|3] [--url URL]

""")


if __name__ == "__main__":
    main()
