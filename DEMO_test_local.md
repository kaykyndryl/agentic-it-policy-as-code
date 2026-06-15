# Demo: Understanding test_local.py

This guide explains how the local testing script (`test_local.py`) works and walks through the IT policies and sample tickets that power the system demonstration.

## 🎯 What is test_local.py?

The local test script is a non-cloud testing utility that:
- ✅ Does NOT require Azure Foundry credentials
- ✅ Demonstrates all 5 integrated tools in action
- ✅ Shows how the system evaluates policies and tickets
- ✅ Validates that all components work correctly
- ✅ Provides a quick way to understand the system before cloud deployment

## 📋 Part 1: Understanding the IT Policies

The system is governed by **8 corporate IT policies**. Each policy defines requirements, compliance levels, and enforcement mechanisms.

### Policy Structure

```text
{
  "id": "POL-001",
  "category": "password_management", 
  "title": "Password Security Policy",
  "description": "Establishes minimum password requirements...",
  "key_requirements": [
    "Minimum 12 characters",
    "Must contain uppercase, lowercase, numbers, special chars",
    "Password reset required every 90 days"
  ],
  "compliance_level": "mandatory",
  "enforcement": "Active Directory"
}
```

### The 8 Policies Explained

#### 1️⃣ POL-001: Password Management
**Purpose**: Ensure strong authentication through password security
- **Requirements**: 12+ characters with mixed case, numbers, special chars
- **Action**: 90-day password resets, no reuse of last 5 passwords
- **Risk**: Account compromise if weak passwords allowed
- **Enforcement**: Active Directory
- **When Violated**: Password reset requests, weak password attempts

#### 2️⃣ POL-002: Multi-Factor Authentication (MFA)
**Purpose**: Prevent unauthorized access to critical systems
- **Requirements**: MFA mandatory for VPN, cloud apps, admin accounts
- **Methods**: TOTP, hardware tokens, Windows Hello
- **Enforcement**: Identity Provider
- **Risk**: Unauthorized access if MFA not enforced
- **When Violated**: VPN/MFA failures, cloud app access issues

#### 3️⃣ POL-003: Data Classification & Handling
**Purpose**: Protect sensitive company and customer data
- **Levels**: Public, Internal, Confidential, Restricted
- **Requirements**: Encryption for Restricted data, access controls
- **Enforcement**: Data Loss Prevention (DLP)
- **Risk**: Data breach or regulatory violations
- **When Violated**: Unauthorized data sharing, exposed file shares

#### 4️⃣ POL-004: Patch Management
**Purpose**: Keep systems secure and up-to-date
- **Timeline**: 
  - Critical/Security patches: 5 days
  - Important patches: 30 days
  - Standard patches: 60 days
- **Enforcement**: SCCM/Intune
- **Risk**: Unpatched vulnerabilities exploited by attackers
- **When Violated**: Systems running outdated versions

#### 5️⃣ POL-005: Access Control
**Purpose**: Ensure proper user provisioning and compliance
- **Requirements**: 
  - Business justification for all access
  - Manager approval required
  - Quarterly access reviews
  - Account removal within 24 hours of termination
- **Enforcement**: Identity Governance
- **Risk**: Unauthorized data access or overprivileged accounts
- **When Violated**: New access requests, access approvals

#### 6️⃣ POL-006: Device Management
**Purpose**: Secure endpoints and enforce compliance baseline
- **Requirements**:
  - Mobile Device Management (MDM) enrollment
  - Security baseline applied to all devices
  - Antivirus and encryption mandatory
- **Enforcement**: Intune/MDM
- **Risk**: Compromised endpoints, malware infection
- **When Violated**: Unenrolled devices, missing antivirus

#### 7️⃣ POL-007: Incident Response
**Purpose**: Rapid response to security incidents
- **Timeline**:
  - Report to Security team: within 1 hour
  - Initial assessment: within 4 hours
  - Forensic evidence preservation: mandatory
  - Management notification: for critical incidents
- **Enforcement**: Security Operations Center (SOC)
- **Risk**: Incident escalation delay, evidence loss
- **When Violated**: Security incidents detected

#### 8️⃣ POL-008: Acceptable Use
**Purpose**: Define appropriate system usage
- **Restrictions**: No unauthorized software, personal use limits
- **Enforcement**: Monitoring and logs
- **Risk**: System misuse, malware introduction
- **When Violated**: Suspicious software installation, policy violations

---

## 🎫 Part 2: Sample Tickets Explained

The demo includes **7 realistic IT support tickets** spanning all 3 risk levels. Each ticket demonstrates different policy implications and routing decisions.

### Sample Tickets Overview

| Ticket ID | Title | Risk Level | Department | Policy |
|-----------|-------|-----------|-----------|--------|
| TKT-001 | Password Reset | **Level 1** | Finance | POL-001 |
| TKT-002 | Cannot Access VPN - MFA Issues | **Level 2** | Engineering | POL-002 |
| TKT-003 | Suspicious Email Download - Malware | **Level 3** | Sales | POL-007 |
| TKT-004 | Monitor Disconnected - Hardware Issue | **Level 1** | Marketing | (None) |
| TKT-005 | Unauthorized File Share - Data Exposure | **Level 3** | Security | POL-003/005 |
| TKT-006 | Printer Driver Installation | **Level 1** | Operations | (None) |
| TKT-007 | Database Access Approval Request | **Level 2** | HR | POL-005 |

### Detailed Ticket Scenarios

#### 🟢 LEVEL 1: TKT-001 - Password Reset Request

```
Ticket ID: TKT-001
Status: New
Title: Password Reset Request
Reported by: john.smith@company.com (Finance Department)
Severity: High
Description: User forgot password and cannot log in to work account
Affected Systems: Active Directory, Email
Policy Implications: POL-001 (Password Management)
```

**Analysis**:
- **Why Level 1**: Common issue with standard remediation
- **Policy**: POL-001 requires password resets every 90 days - this is expected
- **Automated Action**: 
  - Send password reset link
  - Verify identity
  - Set temporary password
  - Force change on next login
- **Estimated Time**: 5-10 minutes
- **Success Rate**: 95%+ (unless account locked)

**Agent Flow**:
```
TicketAnalyzerAgent → Identifies: Password reset, AD policy
RiskAssessmentAgent → Calculates: Low risk (common issue)
RoutingAgent → Routes: AUTO-REMEDIATE (send reset link)
```

#### 🟢 LEVEL 1: TKT-004 - Monitor Disconnected

```
Ticket ID: TKT-004
Status: New
Title: Monitor Disconnected - Hardware Issue
Reported by: sarah.jones@company.com (Marketing)
Severity: Medium
Description: Dual monitor setup - second monitor not recognized after reboot
Affected Systems: Display Adapter, USB
Policy Implications: None
```

**Analysis**:
- **Why Level 1**: Standard hardware troubleshooting with known fixes
- **No Policies Violated**: Hardware issue, no compliance angle
- **Automated Actions**:
  - Reseat USB/Display Port connection
  - Update display driver
  - Check BIOS settings
  - Try different port
- **Success Rate**: 85%+ (most common: reconnect or driver)

#### 🟡 LEVEL 2: TKT-002 - VPN/MFA Access Issues

```
Ticket ID: TKT-002
Status: New
Title: Cannot Access VPN - MFA Issues
Reported by: jane.doe@company.com (Engineering)
Severity: Critical
Description: Repeated MFA failures when connecting to VPN
Affected Systems: VPN, MFA
Policy Implications: POL-002 (Multi-Factor Authentication)
```

**Analysis**:
- **Why Level 2**: Requires specialist troubleshooting and verification
- **Policy**: POL-002 mandates MFA for VPN access
- **Blocking**: Employee working from home, needs remote access
- **Specialist Actions**:
  - Verify MFA device/app is working
  - Check MFA configuration in identity provider
  - Reset MFA if necessary
  - Verify VPN client is updated
  - Check for VPN service issues
- **Route To**: Security Operations Team (VPN specialists)
- **Priority**: High (blocking work)

**Agent Flow**:
```
TicketAnalyzerAgent → Identifies: VPN blocked, MFA involved
RiskAssessmentAgent → Calculates: Medium risk (needs expertise)
RoutingAgent → Routes: ESCALATE to Security Operations
```

#### 🟡 LEVEL 2: TKT-007 - Database Access Request

```
Ticket ID: TKT-007
Status: New
Title: Accessing Sensitive Customer Database - Requires Approval
Reported by: hr.team@company.com (HR)
Severity: Medium
Description: New team member needs customer database access for role
Affected Systems: Database, Access Control
Policy Implications: POL-005 (Access Control)
```

**Analysis**:
- **Why Level 2**: Requires approval workflow and compliance verification
- **Policy**: POL-005 requires:
  - Business justification (has it - role requirement)
  - Manager approval (needs to verify)
  - Compliance check (sensitivity level)
- **Specialist Actions**:
  - Verify business justification
  - Get manager approval
  - Classify data sensitivity level
  - Assign appropriate role
  - Log access grant in audit
- **Route To**: Identity Governance Team
- **Timeline**: 24-48 hours (approval process)

#### 🔴 LEVEL 3: TKT-003 - Malware Detection

```
Ticket ID: TKT-003
Status: New
Title: Suspicious Email Download - Potential Malware
Reported by: mark.wilson@company.com (Sales)
Severity: Critical
Description: User downloaded email attachment (claimed software update)
Affected Systems: Endpoints, Email
Policy Implications: POL-003 (Data), POL-007 (Incident Response)
```

**Analysis**:
- **Why Level 3**: Security incident requiring immediate response
- **Policies Violated**:
  - POL-003: Potential data exposure if infected
  - POL-007: Incident response timeline triggered (1-hour report)
- **Immediate Actions**:
  - Alert Security Operations Center (SOC)
  - Isolate endpoint from network
  - Trigger incident response procedures
  - Preserve forensic evidence
  - Notify management
- **Route To**: SOC + Incident Response Team
- **Timeline**: Immediate (within 1 hour per POL-007)
- **Investigation**: 4+ hours for initial assessment

**Agent Flow**:
```
TicketAnalyzerAgent → Identifies: Malware, active incident
RiskAssessmentAgent → Calculates: CRITICAL risk (security breach)
RoutingAgent → Routes: ESCALATE to SOC (POL-007 triggered)
```

#### 🔴 LEVEL 3: TKT-005 - Data Exposure

```
Ticket ID: TKT-005
Status: New
Title: File Share Access - Unauthorized Shared Folder Found
Reported by: security.team@company.com (Security)
Severity: Critical
Description: Network file share with unrestricted access containing customer data
Affected Systems: File Share, Network Storage
Policy Implications: POL-003 (Data Classification), POL-005 (Access Control)
```

**Analysis**:
- **Why Level 3**: Compliance violation with data exposure risk
- **Policies Violated**:
  - POL-003: Restricted data without encryption, unrestricted access
  - POL-005: Access not controlled, no approval trail
- **Compliance Risk**: GDPR/regulatory violations if customer data exposed
- **Immediate Actions**:
  - Restrict share access (remove unauthorized users)
  - Audit who accessed data and when
  - Notify compliance/legal team
  - Determine data scope and sensitivity
  - Launch investigation into creation/cause
  - Potential disclosure notification if data was leaked
- **Route To**: Security Team + Compliance + Management
- **Timeline**: Immediate escalation + investigation

---

## 🧪 Part 3: How test_local.py Works

### Running the Script

```bash
cd /path/to/agentic-it-policy-as-code
python test_local.py
```

### Script Output Sections

#### Section 1: System Summary
```
IT TICKET MANAGEMENT SYSTEM - LOCAL TEST
================================================================================
📊 Loaded 7 sample tickets
📋 Loaded 8 IT policies
```
Shows that all data files loaded successfully.

#### Section 2: Sample Tickets Display
```
TICKET: TKT-001 - Password Reset Request
============================================================
Department: Finance
Severity: high
Systems: Active Directory, Email
Policies: POL-001
Expected Risk Level: 1
```
Displays first 3 tickets with key information.

#### Section 3: Sample Policies Display
```
📋 POL-001: Password Security Policy
   Category: password_management
   Scope: mandatory
   Key Reqs: 4 requirements
```
Shows first 3 policies and their structure.

#### Section 4: Tool Capabilities Demonstration

**1. POLICY LOOKUP TOOL**
```
Policies found for 'multi-factor': 1 policies
```
Demonstrates searching for policies by keyword. Finds POL-002.

**2. TICKET DATABASE TOOL**
```
Retrieved ticket TKT-001:
  Title: Password Reset Request
  Status: new
```
Shows retrieving individual ticket from database.

**3. RISK EVALUATION TOOL**
```
Risk Assessment for TKT-001:
  Risk Score: 15
  Risk Level: 1
  Classification: Low Risk - Automated Solution Available
```
Calculates risk for the first ticket (password reset):
- **Risk Score**: 15/100 (very low)
- **Level**: 1 (automate)
- **Why**: Common issue with documented fix

**4. REMEDIATION TOOL**
```
Remediation for 'Password Reset Request':
  Available: Yes
  Steps: 5 steps
  Time: 5-10 minutes
  Success Rate: 95%
```
Finds automated remediation steps for the issue.
- Step 1: Send password reset email
- Step 2: User clicks reset link
- Step 3: Creates temporary password
- Step 4: User logs in
- Step 5: Forces password change on login

**5. NOTIFICATION/ROUTING TOOL**
```
Routing for TKT-001:
  Routing Type: auto_remediate
  Assigned To: IT Service (Automated)
  Priority: normal
```
Determines routing:
- **Type**: auto_remediate (Level 1)
- **Team**: IT Service handles automatically
- **Workflow**: Send reset link, monitor completion

### Interpreting Risk Scores

The system uses a **0-100 risk scoring algorithm**:

- **0-30**: Level 1 (Low) - Automate
  - Examples: Password reset (15), printer driver (10), monitor issue (12)
  - Action: Auto-remediate with standard procedures

- **31-70**: Level 2 (Medium) - Review
  - Examples: VPN/MFA issues (45), access requests (50)
  - Action: Route to specialists, 24-48 hour timeline

- **71-100**: Level 3 (High) - Escalate
  - Examples: Malware detected (95), data exposure (90)
  - Action: Immediate response, compliance involvement

### Risk Calculation Factors

The risk algorithm considers:
- **System Criticality**: Is it a critical business system?
- **Data Sensitivity**: Does it involve confidential/restricted data?
- **Policy Violations**: Which policies are affected?
- **Impact Scope**: Individual or organization-wide?
- **Compliance Risk**: Regulatory implications?

---

## 🔄 Part 4: End-to-End Demo Flow

### Complete Flow for a Level 2 Ticket

```
1. INPUT
   ↓
   TKT-002: VPN/MFA Issues (jane.doe@company.com)

2. TICKET ANALYZER AGENT
   ├─ Extracts: VPN blocked, MFA device issue
   ├─ Identifies policies: POL-002 (MFA required)
   ├─ Determines impact: Remote work blocked
   └─ Returns: Detailed analysis + policy implications

3. RISK ASSESSMENT AGENT
   ├─ Evaluates: System criticality (High), data risk (Medium)
   ├─ Calculates: Risk score = 48/100
   ├─ Assigns: Level 2 (Medium Risk)
   └─ Returns: Risk level + classification

4. ROUTING AGENT
   ├─ Determines: Level 2 = Specialist needed
   ├─ Routes to: Security Operations Team
   ├─ Sets priority: High (blocking work)
   ├─ Creates: Support ticket with context
   └─ Notifies: On-call specialist

5. OUTPUT
   ↓
   Security Operations Team gets:
   - Full ticket context
   - Policy implications
   - Risk assessment
   - Troubleshooting guide
   - Priority: High
   - Timeline: 1-4 hours
```

---

## 🚀 Next Steps

### 1. Run the Demo
```bash
python test_local.py
```
✅ Verify all tools work and policies load

### 2. Customize for Your Organization
Edit `data/policies.rego` with your policies
Edit `data/sample_tickets.rego` with your real scenarios

### 3. Deploy to Foundry
Once tested:
```bash
# Configure Foundry credentials
cp .env.template .env
# Edit .env with your Foundry project details

# Start the HTTP server
python -m src.main

# Deploy to Azure
# (See README.md for full deployment instructions)
```

### 4. Integrate with Ticketing System
Connect to your IT ticketing system (ServiceNow, Jira, etc.):
- Read incoming tickets
- Process through agents
- Update ticket with risk level
- Route to correct team
- Automation for Level 1 issues

---

## 📊 Sample Output Metrics

After running `test_local.py`, you'll see:

```
Data Loaded:
✅ 7 sample tickets loaded
✅ 8 IT policies loaded
✅ 0 errors

Tool Tests:
✅ PolicyLookupTool: Working (found 1 policy)
✅ TicketDatabaseTool: Working (retrieved TKT-001)
✅ RiskEvaluationTool: Working (scored TKT-001 as Level 1)
✅ RemediationTool: Working (5-step fix available)
✅ NotificationTool: Working (routing configured)

Risk Distribution (7 tickets):
📊 Level 1 (Auto): 3 tickets (TKT-001, TKT-004, TKT-006)
📊 Level 2 (Review): 2 tickets (TKT-002, TKT-007)
📊 Level 3 (Escalate): 2 tickets (TKT-003, TKT-005)

Ready for:
✅ Foundry deployment
✅ Integration with ticketing system
✅ Production use
```

---

## 🎓 Learning Path

1. **Understand Policies**: Read Section 1 to understand the 8 IT policies
2. **Study Tickets**: Read Section 2 to learn how policies apply to real tickets
3. **Run Demo**: Execute `python test_local.py` and observe the output
4. **Review Output**: Match the output to the explanations in Section 3
5. **Customize**: Edit policies and tickets for your organization
6. **Deploy**: Follow README.md to deploy to Azure Foundry

---

**You now understand the complete IT ticket management system architecture, policies, and how the local test demonstrates the agentic workflow!** 🎉
