#!/usr/bin/env python3
"""
Comprehensive Test - Shows Demo Agent Output and OpenRouter Integration
Demonstrates the multi-agent system with realistic sample tickets
"""

import asyncio
import json
import os
from pathlib import Path

async def main():
    """Run comprehensive test with demo agents and sample data"""
    
    print("=" * 100)
    print("🧪 COMPREHENSIVE IT TICKET MANAGEMENT TEST")
    print("=" * 100)
    print()
    
    # Load sample data
    data_path = Path(__file__).parent / "data"
    
    try:
        with open(data_path / "sample_tickets.json") as f:
            tickets_data = json.load(f)
        with open(data_path / "policies.json") as f:
            policies_data = json.load(f)
    except FileNotFoundError as e:
        print(f"❌ Error loading data files: {e}")
        return
    
    print("📊 Loaded Data:")
    print(f"   - {len(tickets_data['tickets'])} sample tickets")
    print(f"   - {len(policies_data['policies'])} IT policies")
    print()
    
    # Import agents
    from src.demo_agents import DemoTicketAnalyzerAgent, DemoRiskAssessmentAgent, DemoRoutingAgent
    from src.tools import PolicyLookupTool
    
    # Initialize agents
    analyzer = DemoTicketAnalyzerAgent()
    risk_assessor = DemoRiskAssessmentAgent()
    router = DemoRoutingAgent()
    
    print("=" * 100)
    print("🤖 DEMO AGENT INITIALIZATION")
    print("=" * 100)
    print(f"✅ TicketAnalyzerAgent initialized")
    print(f"✅ RiskAssessmentAgent initialized")
    print(f"✅ RoutingAgent initialized")
    print()
    
    # Process 3 sample tickets (Low, Medium, High risk)
    tickets_to_process = [
        tickets_data['tickets'][0],  # INC-001 - Password Reset (Low)
        tickets_data['tickets'][1],  # INC-002 - VPN/MFA (Medium)
        tickets_data['tickets'][2]   # INC-003 - Malware (High)
    ]
    
    for idx, ticket in enumerate(tickets_to_process, 1):
        print("=" * 100)
        print(f"TEST {idx}: {ticket['ticket_id']} - {ticket['title']}")
        print("=" * 100)
        print()
        
        # Stage 1: Analysis
        print("📋 STAGE 1: TICKET ANALYSIS (TicketAnalyzerAgent)")
        print("-" * 100)
        print(f"Input Ticket:")
        print(f"  ID: {ticket['ticket_id']}")
        print(f"  Title: {ticket['title']}")
        print(f"  Department: {ticket['department']}")
        print(f"  Severity: {ticket['severity_reported']}")
        print(f"  Urgency: {ticket.get('urgency', 'N/A')}")
        print(f"  Systems: {', '.join(ticket['affected_systems'])}")
        print()
        
        analysis = await analyzer.analyze_ticket(ticket)
        print("✅ Analysis Output (from Demo Agent):")
        print(f"\n{analysis['content']}")
        print()
        
        if analysis['policy_ids']:
            print("📍 Identified Policies:")
            for policy_id in analysis['policy_ids']:
                policy = PolicyLookupTool.get_policy_by_id(policy_id)
                if policy:
                    print(f"  - {policy_id}: {policy['title']}")
                    print(f"    Category: {policy.get('category', 'N/A')}")
                    print(f"    Scope: {policy.get('scope', 'N/A')}")
        print()
        
        # Stage 2: Risk Assessment
        print("📈 STAGE 2: RISK ASSESSMENT (RiskAssessmentAgent)")
        print("-" * 100)
        
        risk_result = await risk_assessor.assess_risk(ticket, analysis['content'])
        print(f"✅ Risk Assessment Output:")
        print(f"  Risk Score: {risk_result['risk_score']}/100")
        print(f"  Risk Level: {risk_result['risk_level']}")
        print(f"  Classification: {risk_result['classification']}")
        print(f"  Confidence: {int(risk_result.get('confidence_score', 0.75) * 100)}%")
        print()
        
        if risk_result.get('reasoning'):
            print(f"📝 Reasoning (from GenAI model):")
            print(f"  {risk_result['reasoning']}")
        print()
        
        print("📊 Calculation Breakdown:")
        breakdown = risk_result.get('calculation_breakdown', {})
        if breakdown:
            print(f"  Base Severity: {breakdown.get('base_severity', 'N/A')}")
            print(f"  Affected Systems: {breakdown.get('affected_systems_count', 0)}")
            print(f"  Policies Affected: {breakdown.get('policies_affected_count', 0)}")
            print(f"  Final Score: {risk_result['risk_score']}/100")
        print()
        
        # Stage 3: Routing
        print("🎯 STAGE 3: ROUTING DECISION (RoutingAgent)")
        print("-" * 100)
        
        routing = await router.route_and_act(ticket, risk_result)
        print(f"✅ Routing Decision:")
        
        # Handle automation type (level 1)
        if routing.get('automation_type'):
            print(f"  Automation Type: {routing['automation_type']}")
            if routing.get('steps'):
                print(f"  Steps:")
                for step in routing['steps']:
                    print(f"    • {step}")
            if routing.get('estimated_time_minutes'):
                print(f"  Estimated Time: {routing['estimated_time_minutes']} minutes")
        
        # Handle team assignment (levels 2 & 3)
        else:
            if routing.get('assigned_team'):
                print(f"  Assigned Team: {routing['assigned_team']}")
            if routing.get('priority'):
                print(f"  Priority: {routing['priority'].upper()}")
            if routing.get('escalation_required'):
                print(f"  Escalation Required: {'✓ YES' if routing['escalation_required'] else '✗ NO'}")
            
            if routing.get('required_info'):
                print(f"  Required Information:")
                for info in routing['required_info']:
                    print(f"    • {info}")
            
            if routing.get('immediate_actions'):
                print(f"  ⚠️  Immediate Actions:")
                for action in routing['immediate_actions']:
                    print(f"    • {action}")
    
    print("=" * 100)
    print("📌 OPENROUTER MODEL INTEGRATION NOTES")
    print("=" * 100)
    print()
    print("💡 In production, when OpenRouter API is available:")
    print()
    print("1. REAL GENAI OUTPUTS:")
    print("   - All 'reasoning' fields above would contain actual LLM responses")
    print("   - Models used: nemetron/nemetron-3-super (or configured model)")
    print("   - Responses would be more detailed and context-aware")
    print()
    print("2. ENHANCED ANALYSIS:")
    print("   - TicketAnalyzerAgent would provide deeper policy analysis")
    print("   - RiskAssessmentAgent would include confidence scores from model")
    print("   - RoutingAgent would optimize team assignments based on workload")
    print()
    print("3. TOKEN USAGE TRACKING:")
    print("   - Each API call tracks token consumption")
    print("   - Useful for cost monitoring and optimization")
    print("   - Model: nemetron/nemetron-3-super via OpenRouter")
    print()
    print("4. CONFIGURATION:")
    print("   - API Endpoint: https://openrouter.io/api/v1")
    print("   - Auth: OPENROUTER_API_KEY environment variable")
    print("   - Model: OPENROUTER_MODEL environment variable")
    print()
    print("=" * 100)
    print("✅ TEST COMPLETE")
    print("=" * 100)
    print()
    print("📍 Next Steps:")
    print("1. Ensure .env has valid OPENROUTER_API_KEY")
    print("2. Run the web server: python run_web.py")
    print("3. Visit http://localhost:8000 for interactive testing")
    print("4. Submit tickets through the web interface to see GenAI analysis")
    print()

if __name__ == "__main__":
    asyncio.run(main())
