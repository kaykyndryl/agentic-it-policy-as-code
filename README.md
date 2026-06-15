# Agentic IT Policy-as-Code — Multi-Agent IT Ticket Management & OPA Policy Builder

An intelligent, policy-aware platform consisting of two integrated applications:

- **IT Ticket Management System** (Port 8111) — Multi-agent AI workflow that automatically analyzes IT support tickets, assesses risk, and routes to the right team or automated remediation.
- **OPA Policy Builder** (Port 8000) — Upload policy documents (PDF/DOCX) and auto-generate deployable Open Policy Agent (OPA) Rego rules for manufacturing IT/OT and government contractor compliance.

Powered by **OpenRouter AI (NVidia Nemotron 3 Super)** with a local offline fallback for 100% uptime.

## 🎯 System Overview

### What This System Does

This agentic AI system automates IT support ticket management by:

1. **Analyzing** incoming tickets against corporate IT policies
2. **Assessing** risk levels (Low/Medium/High) based on severity and impact
3. **Routing** tickets automatically:
   - **Level 1 (Low Risk)**: Auto-remediate with documented solutions
   - **Level 2 (Medium Risk)**: Route to specialist teams for review
   - **Level 3 (High Risk)**: Escalate to management and security teams

### Quick Demo Scenarios

The web UI includes four **one-click demo scenarios** that auto-fill the ticket form:

| Scenario | Severity | Risk Level | Domain |
|----------|----------|------------|--------|
| Lost Laptop (remote worker) | Critical | 3 – Escalate | Device/Data Security |
| Linux Production Server DDoS | Critical | 3 – Escalate | Infrastructure/Security |
| New Employee Onboarding | Low | 1 – Automate | Access Provisioning |
| VPN Access Request | Medium | 2 – Specialist | Network Access |

### Real-World Example Flow

```
User submits ticket: "Can't connect to VPN - MFA not working"
                          ↓
[TicketAnalyzerAgent]
  → Extracts: VPN issue, MFA involved
  → Identifies: POL-002 (MFA Policy) implications
                          ↓
[RiskAssessmentAgent]
  → Evaluates: Critical dependency, potential data access loss
  → Assigns: Risk Level 2 (Medium) - requires troubleshooting
                          ↓
[RoutingAgent]
  → Routes to: Security Operations Team
  → Action: Send to specialists for MFA troubleshooting
  → Priority: High (blocking remote work)
```

### Core Multi-Agent Architecture

**3 Specialized Agents** work together in sequence:

1. **TicketAnalyzerAgent**
   - Extracts ticket metadata (title, description, affected systems)
   - Maps ticket issues to relevant IT policies
   - Identifies compliance implications
   - Returns: Detailed analysis with policy violations

2. **RiskAssessmentAgent**
   - Evaluates severity using risk scoring algorithm
   - Considers: System criticality, data sensitivity, compliance risk
   - Assigns risk level: 1 (Low), 2 (Medium), or 3 (High)
   - Returns: Risk score (0-100), level, and classification

3. **RoutingAgent**
   - For Level 1: Applies automated remediation steps
   - For Level 2-3: Routes to appropriate support teams
   - Creates action plans and notifications
   - Returns: Routing decision and next steps

### Risk Level Classification

**Level 1 - Low Risk (Automate)**
- Common user issues with documented fixes
- No policy violations
- Self-service or quick IT resolution
- Examples: Password reset, printer driver, monitor issues
- Action: Automated remediation or quick reference guide

**Level 2 - Medium Risk (Review)**
- Issues requiring specialist expertise
- Potential policy implications
- Business impact on individual or department
- Examples: VPN/MFA setup, database access approval, vendor software
- Action: Route to appropriate specialist team

**Level 3 - High Risk (Escalate)**
- Security incidents or data exposure
- Compliance violations
- Potential business-wide impact
- Examples: Malware detection, unauthorized data sharing, breach indicators
- Action: Immediate escalation to SOC and management

## 🧠 AI Risk Analysis Engine

### OpenRouter AI Integration

The system uses **OpenRouter AI** to power intelligent risk analysis and decision-making across three specialized agents:

#### 1. **TicketAnalyzerAgent** (Policy Compliance Analysis)
- **AI Model**: OpenRouter - NVidia Nemotron 3 Super ⭐ (primary model)
- **Temperature**: 0.7 (balanced analysis)
- **Function**: 
  - Analyzes tickets against corporate IT policies
  - Extracts key information (title, description, affected systems)
  - Identifies relevant policies and compliance risks
  - Provides structured compliance assessment

#### 2. **RiskAssessmentAgent** (Risk Scoring & Classification)
- **AI Model**: OpenRouter - NVidia Nemotron 3 Super ⭐ (primary model)
- **Temperature**: 0.3 (precise, deterministic scoring)
- **Function**:
  - Evaluates ticket severity using intelligent risk scoring
  - Computes risk score from 0-100 based on multiple factors
  - Classifies tickets into risk levels (1, 2, or 3)
  - Provides reasoning for risk assignment

#### 3. **RoutingAgent** (Action Determination)
- **AI Model**: OpenRouter - NVidia Nemotron 3 Super ⭐ (primary model)
- **Temperature**: 0.5 (balanced decision making)
- **Function**:
  - Routes tickets to appropriate teams or automated remediation
  - For Level 1: Generates automated remediation steps
  - For Level 2-3: Assigns support teams and escalation requirements
  - Specifies priority levels and required information

### Risk Score Calculation

The **RiskAssessmentAgent** computes risk scores using AI-driven analysis of multiple factors:

#### Base Severity Score
| Severity | Points |
|----------|--------|
| Low | 10 |
| Medium | 30 |
| High | 60 |
| Critical | 80 |

#### AI-Enhanced Adjustments
| Factor | Adjustment | Example |
|--------|-----------|---------|
| Critical Keywords | +20 | "malware", "breach", "security", "data exposure", "unauthorized access" |
| Policy Complexity | +10 | When 2+ policies are affected |
| System Criticality | +5 | Database, VLAN, directory services, email, VPN |

#### Risk Level Assignment
```
Risk Score 0-34   → Level 1 (Low) - Automated Solution Available
Risk Score 35-64  → Level 2 (Medium) - Specialist Review Required
Risk Score 65-100 → Level 3 (High) - Escalation Required
```

### AI Workflow Visualization

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📋 IT Support Ticket                                                │
│ (ID | Title | Description | Department | Severity | Systems)       │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 STAGE 1: Policy Analysis (TicketAnalyzerAgent)                   │
│ ├─ OpenRouter AI Processing                                         │
│ ├─ Extracts ticket information                                      │
│ ├─ Matches relevant IT policies                                     │
│ └─ Assesses policy compliance risks                                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️ STAGE 2: Risk Assessment (RiskAssessmentAgent)                   │
│ ├─ OpenRouter AI Processing (Temperature: 0.3 for precision)        │
│ ├─ Calculate Base Severity Score                                    │
│ ├─ Apply AI-Enhanced Adjustments                                    │
│ │  ├─ Keyword Analysis (+20 for critical terms)                     │
│ │  ├─ Policy Impact (+10 if multiple policies)                      │
│ │  └─ System Criticality (+5 for critical infrastructure)           │
│ └─ Assign Risk Level (1, 2, or 3)                                   │
└────────────────────────┬────────────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
    │ Level 1:    │ │ Level 2:    │ │ Level 3:     │
    │ LOW RISK    │ │ MEDIUM RISK │ │ HIGH RISK    │
    │ (< 35)      │ │ (35-65)     │ │ (> 65)       │
    └──────┬──────┘ └──────┬──────┘ └──────┬───────┘
           │               │               │
           ▼               ▼               ▼
    ┌──────────────────────────────────────────────────┐
    │ 🚦 STAGE 3: Routing & Action (RoutingAgent)      │
    │ ├─ OpenRouter AI Processing                      │
    │ └─ Determine appropriate action                  │
    └────────────┬─────────────────────────────────────┘
                 │
    ┌────────────┼─────────────────┐
    │            │                 │
    ▼            ▼                 ▼
┌─────────────┐ ┌──────────────┐ ┌──────────────────┐
│ ⚙️ AUTOMATED │ │ 👥 SPECIALIST│ │ 🚨 ESCALATION   │
│ REMEDIATION │ │ TEAM REVIEW  │ │ & INCIDENT      │
├─────────────┤ ├──────────────┤ │ RESPONSE        │
│• Password   │ │• IT Support  │ ├──────────────────┤
│  Reset      │ │• Security    │ │• SOC + Incident  │
│• Standard   │ │  Team        │ │  Response Team   │
│  Troublesh  │ │• Identity    │ │• Forensic        │
│  Time: 5-10 │ │  Team        │ │  Analysis        │
│  minutes    │ │• Priority:   │ │• Compliance      │
│             │ │  Med/High    │ │  Notification    │
└─────────────┘ └──────────────┘ │• Priority:       │
                                 │  CRITICAL        │
                                 └──────────────────┘
                                        │
                                        ▼
                                  ┌──────────────┐
                                  │ ✅ Action    │
                                  │    Executed  │
                                  └──────────────┘
```

### AI Model Configuration

The system is configured to use OpenRouter AI with NVidia Nemotron 3 Super via standard API client:

```python
# Default Configuration
OPENROUTER_MODEL = "nemetron/nemetron-3-super"  # Cost-effective, fast
OPENROUTER_BASE_URL = "https://openrouter.io/api/v1"

# Temperature Settings (for determinism vs creativity)
TicketAnalyzerAgent.temperature = 0.7      # Balanced analysis
RiskAssessmentAgent.temperature = 0.3      # Precise scoring
RoutingAgent.temperature = 0.5             # Balanced decisions

# Token Limits
TicketAnalyzerAgent.max_tokens = 1000      # Detailed analysis
RiskAssessmentAgent.max_tokens = 500       # Concise scoring
RoutingAgent.max_tokens = 600              # Action specification
```

### Fallback System (Offline Support)

If OpenRouter API is unavailable, the system automatically falls back to **DemoAgents** with rule-based logic, ensuring 100% uptime:

```python
# In src/agents.py create_agents() function
try:
    # Try OpenRouter AI
    client = get_openrouter_client()
    # Verify connectivity...
    return (
        TicketAnalyzerAgent(client),      # AI-powered
        RiskAssessmentAgent(client),      # AI-powered
        RoutingAgent(client)              # AI-powered
    )
except Exception:
    # Fallback to deterministic logic
    from src.demo_agents import (
        DemoTicketAnalyzerAgent,
        DemoRiskAssessmentAgent,
        DemoRoutingAgent
    )
    return (
        DemoTicketAnalyzerAgent(),        # Rule-based
        DemoRiskAssessmentAgent(),        # Rule-based
        DemoRoutingAgent()                # Rule-based
    )
```

### Built-in IT Policy Framework

8 comprehensive corporate IT policies govern all decisions:

| Policy | Category | Focus | Risk Focus |
|--------|----------|-------|-----------|
| **POL-001** | Password Management | Security baselines for authentication | Account compromise |
| **POL-002** | Multi-Factor Authentication | MFA for remote and sensitive access | Unauthorized access |
| **POL-003** | Data Classification & Handling | Data encryption, access, and sharing | Data breach/exposure |
| **POL-004** | Patch Management | Security update deployment timelines | Unpatched vulnerabilities |
| **POL-005** | Access Control | User provisioning and approval workflow | Unauthorized access |
| **POL-006** | Device Management | Device enrollment, MDM, security baseline | Compromised endpoints |
| **POL-007** | Incident Response | Security incident reporting and procedures | Incident escalation delay |
| **POL-008** | Acceptable Use | User behavior and system usage policies | Policy violations |

### Built-in Integrated Tools

5 specialized tools power the agents:

1. **PolicyLookupTool** - Search and retrieve IT policies by keyword or category
2. **TicketDatabaseTool** - Access and query ticket information
3. **RiskEvaluationTool** - Calculate risk scores based on ticket attributes
4. **RemediationTool** - Lookup automated solutions for Level 1 issues
5. **NotificationTool** - Route tickets and notify support teams

## 📋 Project Structure

```
agentic-it-policy-as-code/
├── app.py                      # OPA Policy Builder — FastAPI app (port 8000)
├── run_web.py                  # Startup script for OPA Policy Builder
├── src/
│   ├── __init__.py
│   ├── main.py                 # IT Ticket Management — aiohttp server (port 8111)
│   ├── agents.py               # AI agents via OpenRouter (Analyzer, Risk, Router)
│   ├── demo_agents.py          # Offline fallback agents (rule-based, no API needed)
│   ├── opa_policy_builder.py   # OPA Rego rule generator (50 rules: IT + MFG + GOV)
│   ├── workflow.py             # Multi-agent orchestration pipeline
│   └── tools.py                # Tool implementations (PolicyLookup, Risk, Routing)
├── data/
│   ├── policies.json           # 8 corporate IT policies database
│   ├── sample_tickets.json     # Sample tickets for testing (all 3 risk levels)
│   └── generated_policies.rego # Last auto-generated OPA Rego policy file
├── .vscode/
│   ├── launch.json             # Debug configurations
│   └── tasks.json              # VS Code build tasks
├── .env.template               # Configuration template (placeholder values only)
├── agent.yaml                  # Agent configuration and workflow definition
├── requirements.txt            # Python dependencies
├── test_local.py               # Local offline testing script
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenRouter API key (free account at https://openrouter.ai)
- VS Code with Python extension (for debugging)

### 1. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify using correct Python
which python  # Should show venv path
```

### 2. Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

Dependencies include:
- `openai>=1.3.0` - Standard API client for OpenRouter (NVidia Nemotron 3 Super)
- `python-dotenv` - Environment variable management
- `aiohttp` - Async HTTP client/server library
- `pydantic` - Data validation

### 3. Configure OpenRouter Access

Get your free OpenRouter API key:

1. Visit https://openrouter.ai
2. Sign up and get your API key
3. Copy `.env.template` to `.env`:

```bash
cp .env.template .env
```

Edit `.env` and configure:

```env
# OpenRouter AI Configuration
OPENROUTER_API_KEY=<your-openrouter-api-key>
OPENROUTER_MODEL=nemetron/nemetron-3-super
OPENROUTER_BASE_URL=https://openrouter.io/api/v1

# Application settings
LOG_LEVEL=INFO
DEBUG_MODE=false
```

Available models at OpenRouter:
- `nemetron/nemetron-3-super` - NVidia Nemotron 3 Super (⭐ Primary - recommended)
- `nemetron/nemetron-3-super` - NVidia Nemotron 3 Super (primary, recommended)
# Alternative providers (not recommended for this system):
# - ~~`openai/gpt-4-turbo`~~ - (Alternative, requires separate API key)
# - ~~`openai/gpt-4`~~ - (Alternative, requires separate API key)
# - ~~`anthropic/claude-3-opus`~~ - (Alternative, not recommended)
- See https://openrouter.ai/models for full list

### 4. Test the System Locally

Test the agents and tools without cloud deployment:

```bash
python test_local.py
```

This will:
- Load sample policies and tickets
- Test all tool implementations
- Display risk assessments for sample tickets
- Verify system readiness

Sample output:
```
📊 Loaded 7 sample tickets
📋 Loaded 8 IT policies
1. POLICY LOOKUP TOOL
   Policies found for 'multi-factor': 1 policies
2. TICKET DATABASE TOOL
   Retrieved ticket TKT-001: Password Reset Request
3. RISK EVALUATION TOOL
   Risk Score: 15, Risk Level: 1
...
✅ LOCAL TEST COMPLETE
```

### 5. Start Both Services

**IT Ticket Management System** (Port 8111):
```bash
python -m src.main
```
Available at `http://localhost:8111`

**OPA Policy Builder** (Port 8000):
```bash
python run_web.py
```
Available at `http://localhost:8000` — upload a policy PDF/DOCX and download generated Rego rules.

Example ticket API request:
```bash
curl -X POST http://localhost:8111/tickets/process \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TKT-001",
    "title": "Password Reset Request",
    "description": "User forgot their password",
    "department": "Finance",
    "affected_systems": ["Active Directory", "Email"],
    "severity_reported": "high",
    "policy_implications": ["POL-001"]
  }'
```

## 🔧 Development & Debugging

### VS Code Debug Configurations

The project includes two debug configurations in `.vscode/launch.json`:

1. **Python: Run Local Test** - Run the test suite
2. **Python: Run Main Server** - Start the HTTP server

#### Debug with F5

Press `F5` to start debugging. You'll see:
- Console output from agents
- Multi-agent workflow execution
- Risk assessment scores
- Routing decisions
   - Response traces

### Available VS Code Tasks

Run with Ctrl+Shift+B or Command Palette:

```bash
# Install dependencies
Tasks: Run Task > Install Dependencies

# Run tests
Tasks: Run Task > Run Local Test

# Start server
Tasks: Run Task > Start HTTP Server

# Format code
Tasks: Run Task > Format Code

# Lint code
Tasks: Run Task > Lint Code
```

## 📊 Workflow Execution

### Processing Flow

```
┌─────────────────────────┐
│   Incoming IT Ticket    │
└────────────┬────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│   STAGE 1: TICKET ANALYSIS           │
│   - Agent: TicketAnalyzerAgent       │
│   - Extracts ticket information      │
│   - Checks against IT policies       │
│   - Identifies compliance risks      │
└────────────┬─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│   STAGE 2: RISK ASSESSMENT           │
│   - Agent: RiskAssessmentAgent       │
│   - Computes risk score (0-100)      │
│   - Classifies severity level        │
│   - Identifies approvals needed      │
└────────────┬─────────────────────────┘
             │
        ┌────┴─────────────────────┐
        │                          │
        ▼                          ▼
┌─────────────────┐      ┌──────────────────┐
│ LEVEL 1 (Low)   │      │ LEVEL 2-3 (High) │
├─────────────────┤      ├──────────────────┤
│ Automated Fix   │      │ Route to Team    │
│ - Execute steps │      │ - Assign owner   │
│ - Auto remediate│      │ - Escalate       │
│ - Notify user   │      │ - Notify team    │
└─────────────────┘      └──────────────────┘
```

### Example: Processing a Ticket

```python
from src.workflow import create_workflow
from src.tools import TicketDatabaseTool

# Create workflow
workflow = await create_workflow()

# Get a ticket
db = TicketDatabaseTool()
ticket = await db.execute(operation="get", ticket_id="TKT-001")

# Process through workflow
result = await workflow.process_ticket(ticket)

# Result includes:
# - analysis: Policy compliance analysis
# - risk_assessment: Risk level and score
# - routing: Final routing decision
# - final_action: Assigned team or automation steps
```

## 🛠️ Tools & Capabilities

### PolicyLookupTool

Search and retrieve IT policies:

```python
tool = PolicyLookupTool()

# Search by keyword
await tool.execute(search_type="keyword", query="multi-factor")

# Search by category
await tool.execute(search_type="category", query="access_control")

# Get specific policy
await tool.execute(search_type="id", query="POL-001")

# List all policies
await tool.execute(search_type="all", query="")
```

### TicketDatabaseTool

Access ticket information:

```python
tool = TicketDatabaseTool()

# Get specific ticket
await tool.execute(operation="get", ticket_id="TKT-001")

# List tickets by department
await tool.execute(operation="list_by_department", department="Finance")

# List all tickets
await tool.execute(operation="list_all", query="")
```

### RiskEvaluationTool

Evaluate ticket risks:

```python
tool = RiskEvaluationTool()

# Analyze ticket for risk
await tool.execute(ticket_data=ticket_dict)

# Returns: risk_score, risk_level, classification
```

### RemediationTool

Get automated fixes:

```python
tool = RemediationTool()

# Suggest remediation for ticket type
await tool.execute(
    ticket_title="Password Reset Request",
    issue_category="authentication"
)

# Returns: remediation steps, time estimate, success rate
```

### NotificationTool

Route tickets and notify teams:

```python
tool = NotificationTool()

# Route ticket
await tool.execute(
    ticket_id="TKT-001",
    risk_level=2,
    policy_ids=["POL-001"]
)

# Returns: routing decision, assigned team, priority
```

## 🚀 Deployment

### Environment Configuration

Copy `.env.template` to `.env` and fill in your API key:

```env
OPENROUTER_API_KEY=<your-openrouter-api-key>
OPENROUTER_MODEL=nemetron/nemetron-3-super
OPENROUTER_BASE_URL=https://openrouter.io/api/v1
LOG_LEVEL=INFO
DEBUG_MODE=false
```

> ⚠️ Never commit `.env` — it is excluded by `.gitignore`. Only `.env.template` (with placeholder values) is tracked in the repository.

### Running Both Services Locally

```bash
# Terminal 1 — IT Ticket Management (port 8111)
python -m src.main

# Terminal 2 — OPA Policy Builder (port 8000)
python run_web.py
```

### Health Checks

```bash
# IT Ticket Management
curl http://localhost:8111/health

# OPA Policy Builder API docs
curl http://localhost:8000/api/docs
```

## 📈 Monitoring & Logging

### Local Logging

Logs are configured via `LOG_LEVEL` environment variable:

```env
LOG_LEVEL=DEBUG    # Verbose logging for development
LOG_LEVEL=INFO     # Standard logging for production
LOG_LEVEL=WARNING  # Only warnings and errors
```

### Azure Monitor Integration (Deployed)

When deployed, leverage Application Insights for:
- Request tracking
- Error monitoring
- Performance metrics
- Custom events

```python
# In application code
logger.info("Processing ticket", extra={
    "ticket_id": ticket_id,
    "risk_level": risk_level
})
```

## 🧪 Testing

### Run Local Tests

```bash
python test_local.py
```

Tests cover:
- Tool functionality verification
- Sample data loading
- Risk assessment calculations
- Ticket routing logic

### Manual Testing via HTTP

Using curl or Postman:

```bash
# Test agent endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Process ticket TKT-001"}
    ]
  }'
```

### Performance Testing

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:8000/

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/chat
```

## 🔐 Security Considerations

### Best Practices

1. **Credentials Management**
   - Never commit `.env` with real credentials
   - Use managed identities in production
   - Rotate credentials regularly

2. **Data Protection**
   - Tickets may contain sensitive information
   - Implement audit logging for all ticket access
   - Encrypt data in transit (HTTPS)
   - Implement role-based access control

3. **API Security**
   - Require authentication for agent endpoints
   - Implement rate limiting
   - Use CORS policies appropriately
   - Validate all inputs

4. **Audit & Compliance**
   - Log all ticket processing
   - Track routing decisions
   - Document manual overrides
   - Regular compliance audits

## 📞 Support & Troubleshooting

### Common Issues

**Issue: "API key error / connection refused"**
```
Solution: Ensure .env has a valid OPENROUTER_API_KEY:
  cat .env | grep OPENROUTER_API_KEY
If blank, the system falls back to local demo agents automatically.
```

**Issue: "Module not found"**
```
Solution: Install dependencies and activate your virtual environment:
  source venv/bin/activate
  pip install -r requirements.txt
```

**Issue: "Port already in use"**
```
Solution:
  # Kill process on port 8111
  lsof -i :8111 | awk 'NR>1{print $2}' | xargs kill -9
  # Kill process on port 8000
  lsof -i :8000 | awk 'NR>1{print $2}' | xargs kill -9
```

### Debug Checklist

- [ ] Virtual environment activated
- [ ] `pip install -r requirements.txt` completed
- [ ] `.env` file created from `.env.template` with your API key
- [ ] Python 3.9+ version verified
- [ ] Local test passes: `python test_local.py`
- [ ] Both services started: port 8111 (tickets) and port 8000 (OPA)

## 📚 Additional Resources

- [OpenRouter AI](https://openrouter.ai) — API gateway for NVidia Nemotron 3 Super and other models
- [Open Policy Agent](https://www.openpolicyagent.org) — Rego policy engine
- [aiohttp Documentation](https://docs.aiohttp.org) — Async HTTP server framework
- [FastAPI Documentation](https://fastapi.tiangolo.com) — OPA Policy Builder framework

## 📝 Next Steps

1. **Extend Policies**: Add custom IT policies for your organization in `data/policies.json`
2. **Upload Your Own Policy Docs**: Use the OPA Policy Builder (port 8000) to generate Rego rules from your own PDF/DOCX policy files
3. **Custom Tools**: Implement connectors for ticketing platforms (ServiceNow, Jira, etc.)
4. **Integration**: Connect to actual ticket databases and communication platforms
5. **Scoring Tuning**: Adjust risk score thresholds in `src/demo_agents.py` for your environment
6. **Add Demo Scenarios**: Extend the demo tickets in `src/main.py` DEMO_TICKETS dict

## ✨ Architecture Highlights

- **Two Integrated Services**: IT Ticket Management (port 8111) + OPA Policy Builder (port 8000)
- **Multi-Agent Orchestration**: Specialized agents for analysis, assessment, and routing
- **Policy-Driven**: All decisions based on IT policies (manufacturing IT/OT + government contractor + general IT)
- **OPA Rego Generation**: 50 deterministic deny rules covering IT change control, manufacturing OT, and government compliance (ITAR, FISMA, CUI)
- **Dark Developer UI**: High-contrast dark theme with CSS custom properties, optimized for extended use
- **One-Click Demo Scenarios**: Four pre-loaded clickable demo tickets auto-fill the form for instant testing
- **Transparent Risk Scoring**: Full scoring breakdown (base + keyword + system + policy factors) displayed in results
- **Async/Await**: Efficient async processing for scalability
- **Offline Fallback**: Local demo agents automatically used when OpenRouter API is unavailable
- **Security Hardened**: `.env` git-ignored, `.env.template` with placeholders only, no secrets in repository

## 📄 License

Copyright (c) 2026. All rights reserved.
