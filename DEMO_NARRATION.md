# IT Ticket Management System — Demo Narration Guide

## 🎬 Opening Narration

Welcome to the **AI-Powered IT Ticket Management System** — a multi-agent platform that intelligently analyzes, classifies, and routes IT support tickets while enforcing corporate IT policies as code.

This system demonstrates how agentic AI and policy-as-code work together to make smarter, faster decisions that protect your organization while reducing manual workload.

The web interface at **http://localhost:8111** includes four one-click demo scenarios that auto-fill the form for instant testing.

---

## 🎯 Four Demo Scenarios

### 💻 Scenario 1: Lost Laptop — Level 3 (Critical Escalation)

**Click:** `💻 Lost Laptop` demo button

**Ticket Details auto-filled:**
- **ID:** INC-DEMO-001
- **Title:** Lost company laptop — remote worker
- **Description:** Employee reports company-issued laptop containing sensitive project files was lost at an airport. Device may be unencrypted. Last sync 48 hours ago.
- **Department:** Engineering
- **Severity:** Critical
- **Affected Systems:** Endpoints, Active Directory
- **Policies:** POL-003 (Data Classification), POL-006 (Device Management)

**What the agents do:**

1. **TicketAnalyzerAgent** identifies: lost device, potential data exposure, device management policy violation (POL-006), data classification concern (POL-003)

2. **RiskAssessmentAgent** computes:
   - Severity base: 80 pts (Critical)
   - Critical keyword boost: +20 pts ("sensitive", "unencrypted", "data")
   - System criticality: +5 pts (Active Directory)
   - **Final score: ~95/100 → Level 3 (High Risk)**

3. **RoutingAgent** escalates to: SOC + Incident Response Team, triggers device remote wipe procedure, notifies compliance

**Key talking points:**
- Policy-as-code auto-identifies data classification and device management violations
- Critical severity + data exposure keywords drive maximum risk score
- Immediate escalation with documented remediation steps

---

### 🔴 Scenario 2: DDoS Attack — Level 3 (Critical Escalation)

**Click:** `🔴 DDoS Attack` demo button

**Ticket Details auto-filled:**
- **ID:** INC-DEMO-002
- **Title:** Linux production server overloaded — possible DDoS
- **Description:** Production Linux server experiencing abnormal traffic spike. CPU at 100%, services unresponsive. Network team suspects DDoS attack targeting port 443. Business operations affected.
- **Department:** Engineering
- **Severity:** Critical
- **Affected Systems:** Database, Endpoints
- **Policies:** POL-004 (Patch Management), POL-007 (Incident Response)

**What the agents do:**

1. **TicketAnalyzerAgent** identifies: active security incident, production system impact, incident response policy triggers (POL-007), potential patch/vulnerability concern (POL-004)

2. **RiskAssessmentAgent** computes:
   - Severity base: 80 pts (Critical)
   - Critical keyword boost: +20 pts ("DDoS", "attack", "unresponsive")
   - System criticality: +5 pts (Database)
   - Policy impact: +10 pts (multiple policies)
   - **Final score: ~100/100 → Level 3 (High Risk)**

3. **RoutingAgent** escalates to: Network Security Team + SOC, activates incident response, blocks suspicious IPs, initiates DDoS mitigation

**Key talking points:**
- Multiple critical keywords drive maximum boost to risk score
- Two policy triggers (incident response + patch management) add policy impact points
- Real-time scoring transparency shows each contributing factor

---

### 👤 Scenario 3: New Employee Onboarding — Level 1 (Automated)

**Click:** `👤 New Employee Onboarding` demo button

**Ticket Details auto-filled:**
- **ID:** INC-DEMO-003
- **Title:** New employee system access setup
- **Description:** New employee starting Monday needs standard system access: email, VPN, shared drive, and project management tools. Manager has approved standard access package.
- **Department:** HR
- **Severity:** Low
- **Affected Systems:** Active Directory, Email
- **Policies:** POL-005 (Access Control)

**What the agents do:**

1. **TicketAnalyzerAgent** identifies: standard provisioning request, access control policy (POL-005), manager approval documented

2. **RiskAssessmentAgent** computes:
   - Severity base: 10 pts (Low)
   - No critical keywords
   - Standard systems only
   - Single policy
   - **Final score: ~15/100 → Level 1 (Low Risk)**

3. **RoutingAgent** routes to: Automated Provisioning workflow
   - Create AD account
   - Provision email and calendar
   - Configure VPN access
   - Grant standard drive access
   - Send welcome kit with credentials

**Key talking points:**
- Clean ticket with no risk indicators = automated handling
- Policy compliance verified (access control, manager approval noted)
- No human intervention needed — system handles end-to-end

---

### 🔐 Scenario 4: VPN Access Request — Level 2 (Specialist Review)

**Click:** `🔐 VPN Access Request` demo button

**Ticket Details auto-filled:**
- **ID:** INC-DEMO-004
- **Title:** VPN access request for remote work
- **Description:** Employee requesting VPN access for full-time remote work. Needs access to internal development servers and database environments. Working from home office with personal device.
- **Department:** IT
- **Severity:** Medium
- **Affected Systems:** VPN, Database
- **Policies:** POL-002 (MFA Policy), POL-005 (Access Control)

**What the agents do:**

1. **TicketAnalyzerAgent** identifies: access escalation request, MFA enforcement required (POL-002), access approval workflow (POL-005), personal device concern

2. **RiskAssessmentAgent** computes:
   - Severity base: 30 pts (Medium)
   - System criticality: +5 pts (Database)
   - Policy impact: +10 pts (two policies)
   - **Final score: ~45/100 → Level 2 (Medium Risk)**

3. **RoutingAgent** routes to: Security Operations Center (Identity & Access Team)
   - Verify device compliance or MDM enrollment
   - Enforce MFA configuration
   - Approve database access scope
   - Create conditional access policy

**Key talking points:**
- Personal device + database access = specialist review required
- Two policy triggers (MFA + access control) contribute to score
- Level 2 keeps a human in the loop for access decisions

---

## 📊 OPA Policy Builder Demo (Port 8000)

Open `http://localhost:8000` in a second browser tab.

**Demo flow:**
1. Upload any corporate IT policy PDF or DOCX
2. Show the extracted policy statements in the generated Rego header
3. Walk through sample deny rules:
   - `IT-002`: High-risk change requires CAB approval
   - `MFG-009`: OT network changes require ICS security review
   - `GOV-001`: ITAR-controlled code changes require export compliance review
4. Download the `.rego` file — ready to deploy to an OPA instance

**Key talking points:**
- 50 deny rules covering three compliance domains: IT, manufacturing OT, government contractor
- Document traceability: extracted sentences appear as comments in the Rego file
- No healthcare context — aligned to manufacturing and government contractor workflows

---

## ✅ Demo Checklist

Before presenting:
- [ ] Both services running: `python -m src.main` (8111) and `python run_web.py` (8000)
- [ ] Browser tabs open: `http://localhost:8111` and `http://localhost:8000`
- [ ] `.env` configured with a valid `OPENROUTER_API_KEY` (or confirm demo agents will be used)
- [ ] Test one demo button click to confirm form auto-fill works
