# 🚀 Quick Start Guide - Enhanced IT Policy as Code System

## ✨ What's New

### 1. **Policy Identification** ✅
- System now **auto-identifies relevant policies** based on ticket content
- Shows detailed policy information:
  - Policy ID and Title
  - Category and Description  
  - Enforcement mechanism
  - Key compliance requirements

### 2. **Smart Team Assignment** ✅
- **Level 1 (Low Risk):** Automated remediation with specific steps
- **Level 2 (Medium Risk):** Specialist team assignment
- **Level 3 (High Risk):** Critical escalation with immediate actions

### 3. **Automation Agents** ✅
- System recommends which AI agents should handle each ticket
- Examples:
  - Password Reset Agent → for password issues
  - MFA Troubleshooting Agent → for VPN/MFA issues
  - Malware Analysis Agent → for security incidents
  - Forensic Collection Agent → for breach investigations

### 4. **Demo Script** ✅
- New `web_demo_test.py` for testing
- 3 built-in example scenarios
- Both manual and API testing modes

---

## 🎯 Quick Test

### Step 1: Start the Server
```bash
cd /path/to/agentic-it-policy-as-code
source venv/bin/activate
python run_web.py
```
Expected output:
```
🚀 IT TICKET MANAGEMENT SYSTEM - WEB SERVER
📍 Server starting on: http://0.0.0.0:8000
```

### Step 2: Run Demo Script (Option A - Manual JSON)
```bash
python web_demo_test.py
```
This displays 3 formatted JSON tickets you can copy-paste into the web form.

### Step 3: Run Demo Script (Option B - Auto Test)
```bash
# Test all 3 scenarios
python web_demo_test.py --api

# Test specific scenario (1=Password, 2=VPN, 3=Security)
python web_demo_test.py --api --ticket 1
```

### Step 4: Open Web Interface
Visit: http://localhost:8000

---

## 📊 What You'll See

### For Level 1 Tickets (e.g., Password Reset)
```
Risk Score: 20/100
Risk Level: 1 (Low Risk)

📋 Identified Policies: POL-001
Policy Details:
  - Password Security Policy
  - Key Requirement: "Password reset required every 90 days"
  - Enforcement: Active Directory

🎯 Recommended Actions:
  Automation Type: password_reset
  Estimated Time: 5 minutes
  Steps:
    1. Trigger password reset link
    2. User creates new password
    3. Verify AD sync
    4. Confirm user login
```

### For Level 2 Tickets (e.g., VPN/MFA)
```
Risk Score: 48/100
Risk Level: 2 (Medium Risk)

📜 Identified Policies: POL-002, POL-005
Policy Details:
  - MFA Policy + Access Control Policy

👥 Assigned Team: Security Operations Center (SOC) - Identity & Access Team
Priority: HIGH
🤖 Automation Agents:
  - MFA Troubleshooting Agent
  - VPN Connectivity Diagnostics

📋 Required Information:
  - MFA device used
  - Error messages
  - Last successful connection time
```

### For Level 3 Tickets (e.g., Security Alert)
```
Risk Score: 85/100
Risk Level: 3 (High Risk)

📜 Identified Policies: POL-003, POL-004, POL-006, POL-007
Policies: Data Classification, Patch Management, Device Management, Incident Response

👥 Assigned Team: SOC + Incident Response Team
Priority: CRITICAL ⚠️
🤖 Automation Agents:
  - Malware Analysis Agent
  - Forensic Collection Agent

🚨 Immediate Actions (8+ critical steps):
  ⚡ Isolate affected endpoint
  ⚡ Preserve forensic evidence
  ⚡ Notify Compliance team
  ⚡ Begin investigation
  ⚡ Contact affected users
  ...
```

---

## 📋 Example Test Tickets

### Test 1: Password Reset (Level 1)
```json
{
  "ticket_id": "TKT-DEMO-001",
  "title": "Password Reset Request",
  "description": "User forgot their password",
  "department": "Finance",
  "affected_systems": ["Active Directory", "Email"],
  "severity_reported": "high",
  "policy_implications": ["POL-001"]
}
```

### Test 2: VPN/MFA Issue (Level 2)
```json
{
  "ticket_id": "TKT-DEMO-002",
  "title": "Cannot Access VPN - MFA Failures",
  "description": "MFA timeouts when connecting to corporate VPN",
  "department": "Engineering",
  "affected_systems": ["VPN", "MFA"],
  "severity_reported": "critical",
  "policy_implications": ["POL-002"]
}
```

### Test 3: Security Alert (Level 3)
```json
{
  "ticket_id": "TKT-DEMO-003",
  "title": "Suspicious Email Download - Malware Detected",
  "description": "User opened suspicious attachment. Antivirus alerts triggered.",
  "department": "Sales",
  "affected_systems": ["Endpoints", "Email", "Network"],
  "severity_reported": "critical",
  "policy_implications": ["POL-003", "POL-007"]
}
```

---

## 🎯 Key Features Demonstrated

### ✅ Policy Intelligence
- Auto-detects 8 corporate IT policies
- Maps policies to ticket issues
- Shows policy details and requirements

### ✅ Risk Scoring
- Calculates risk score 0-100
- Factors: severity, systems, policies, keywords
- Transparent calculation breakdown

### ✅ Smart Routing
- Level 1 → Automated steps
- Level 2 → Specialist team
- Level 3 → Critical escalation + immediate actions

### ✅ AI-Powered Analysis
- OpenRouter AI for policy analysis
- OpenRouter AI for risk assessment
- OpenRouter AI for action recommendations

### ✅ Automation Agents
- Specific agents for each scenario
- Examples: MFA Troubleshooting, Malware Analysis, Data Classification
- Fallback: Comprehensive rule-based recommendations

---

## 🔄 Full Workflow

```
Ticket Submission
       ↓
Policy Identification (TicketAnalyzerAgent)
       ↓
Risk Assessment (RiskAssessmentAgent)
       ↓
Action Recommendation (RoutingAgent)
       ↓
Display Results:
  - Risk Score Breakdown
  - Identified Policies
  - Policy Details
  - AI Reasoning
  - Recommended Actions
  - Team Assignment
  - Automation Agents
  - Immediate Actions (if critical)
```

---

## 🛠️ File Locations

- **Web Interface:** http://localhost:8000
- **Demo Script:** `web_demo_test.py`
- **Main Code:**
  - `src/agents.py` - Enhanced with policy identification
  - `src/workflow.py` - Updated to track policies
  - `src/tools.py` - Policy lookup tool
- **Configuration:**
  - `.env` - OpenRouter API key
  - `data/policies.json` - All 8 corporate policies
  - `data/sample_tickets.json` - Sample test tickets

---

## 📞 Support

**Testing Policy Identification:**
- Check if ticket is auto-identifying correct policies
- Verify policy details display properly
- Confirm policy requirements are shown

**Testing Risk Scoring:**
- Compare Level 1, 2, and 3 scenarios
- Check if scores correlate with severity
- Verify policies affect risk calculation

**Testing Team Assignment:**
- Confirm Level 1 shows automation steps
- Check Level 2 shows specialist team
- Verify Level 3 shows SOC + immediate actions

---

**All enhancements complete! The system now provides comprehensive policy analysis with intelligent team assignment and automation recommendations.** 🎉
