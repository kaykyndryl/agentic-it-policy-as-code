# IT Ticket Management System - Multi-Agent Workflow

An intelligent, policy-aware IT support ticket management system powered by Microsoft Agent Framework and Azure AI Foundry. The system automatically analyzes tickets, assesses risks, and routes them to appropriate teams or automated remediation based on severity.

## 🎯 System Overview

### What This System Does

This agentic AI system automates IT support ticket management by:

1. **Analyzing** incoming tickets against corporate IT policies
2. **Assessing** risk levels (Low/Medium/High) based on severity and impact
3. **Routing** tickets automatically:
   - **Level 1 (Low Risk)**: Auto-remediate with documented solutions
   - **Level 2 (Medium Risk)**: Route to specialist teams for review
   - **Level 3 (High Risk)**: Escalate to management and security teams

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
├── src/
│   ├── __init__.py
│   ├── main.py                 # HTTP server entry point
│   ├── agents.py               # Agent definitions (Analyzer, Risk Assessor, Router)
│   ├── workflow.py             # Multi-agent orchestration
│   └── tools.py                # Tool implementations (Policy Lookup, Risk Eval, etc.)
├── data/
│   ├── policies.json           # Corporate IT policies database
│   └── sample_tickets.json     # Sample tickets for testing (all risk levels)
├── .vscode/
│   ├── launch.json             # Debug configurations
│   └── tasks.json              # VS Code build tasks
├── .env.template               # Configuration template
├── .env                        # Local configuration (add Foundry credentials)
├── agent.yaml                  # Agent configuration and workflow definition
├── requirements.txt            # Python dependencies (pinned versions)
├── test_local.py              # Local testing script
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Azure Foundry project with deployed model
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

Install packages in the correct order (agentserver first, then agent-framework):

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

### 3. Configure Foundry Access

Copy `.env.template` to `.env` and fill in your Foundry project details:

```bash
cp .env.template .env
```

Edit `.env` with your values:
```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-region>.api.azureml.ms/foundry
FOUNDRY_MODEL_DEPLOYMENT_NAME=<your-model-deployment>
```

### 4. Test the System Locally

Before deploying, test the workflow and tools:

```bash
python test_local.py
```

This will:
- Load sample policies and tickets
- Test all tool implementations
- Display risk assessments for sample tickets
- Verify system readiness

### 5. Run the HTTP Server

Start the agent server for local testing:

```bash
python -m src.main
```

The server will be available at `http://localhost:8000`

## 🔧 Development & Debugging

### VS Code Debug Configurations

The project includes three debug configurations:

1. **Python: Run Main Server** - Start the HTTP server
2. **Python: Run Local Test** - Run the test suite
3. **Python: Debug with AI Toolkit Inspector** - Use Agent Inspector for interactive debugging

#### Debug with F5

Press `F5` to start debugging with the default configuration (Run Main Server).

![Debug Flow](docs/debug-config.png)

#### Using AI Toolkit Agent Inspector

1. Install the AI Toolkit extension in VS Code
2. Open the Command Palette (Cmd/Ctrl+Shift+P)
3. Select "Agent Developer: Start Debugging with Inspector"
4. The Agent Inspector panel will open showing:
   - Agent communications
   - Message flows between agents
   - Tool invocations
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

## 🚀 Deployment to Azure Foundry

### Prerequisites

- Azure Foundry project created
- Model deployed and endpoint available
- Credentials configured

### Deployment Options

#### Option 1: Using VS Code Extension

1. Open Command Palette (Cmd/Ctrl+Shift+P)
2. Run "Microsoft Foundry: Deploy Hosted Agent"
3. Follow the prompts
4. Select this project
5. Configure deployment settings
6. Deploy

#### Option 2: Using Azure CLI

```bash
# Set your subscription
az account set --subscription <subscription-id>

# Deploy to Container Apps (recommended)
az containerapp up \
  --name it-ticket-management \
  --resource-group <resource-group> \
  --ingress external \
  --target-port 8000

# Or deploy to App Service
az appservice plan create \
  --name it-ticket-plan \
  --resource-group <resource-group> \
  --sku B1

az webapp create \
  --name it-ticket-management \
  --resource-group <resource-group> \
  --plan it-ticket-plan \
  --runtime PYTHON:3.11
```

### Environment Configuration for Deployment

Update `.env` with Foundry credentials before deployment:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<region>.api.azureml.ms/foundry
FOUNDRY_MODEL_DEPLOYMENT_NAME=<deployment-name>
LOG_LEVEL=INFO
DEBUG_MODE=false
```

### Health Check

Test deployed endpoint:

```bash
curl -X GET http://<your-host>:8000/health
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

**Issue: "Foundry configuration not set"**
```
Solution: Ensure FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL_DEPLOYMENT_NAME 
are set in .env file
```

**Issue: "Authentication failed"**
```
Solution: Verify Azure credentials with:
  az account show
  az account set --subscription <subscription-id>
```

**Issue: "Module not found"**
```
Solution: Install dependencies in correct order:
  pip install -r requirements.txt
  Ensure virtual environment is activated
```

### Debug Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed correctly
- [ ] .env file configured with Foundry credentials
- [ ] Python 3.10+ version verified
- [ ] Test passes locally: `python test_local.py`
- [ ] Agent Inspector connected (for VS Code debugging)

## 📚 Additional Resources

- [Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry](https://www.microsoft.com/en-us/cloud-platform/azure-ai-foundry)
- [Azure Identity SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity)

## 📝 Next Steps

1. **Extend Policies**: Add custom IT policies for your organization
2. **Custom Tools**: Implement tools for ticket management systems (ServiceNow, Jira, etc.)
3. **Integration**: Connect to actual ticket databases and communication platforms
4. **Analytics**: Add dashboards for ticket processing metrics
5. **Optimization**: Fine-tune risk assessment algorithms and routing logic

## ✨ Architecture Highlights

- **Multi-Agent Orchestration**: Specialized agents for analysis, assessment, and routing
- **Policy-Driven**: All decisions based on IT policies
- **Async/Await**: Efficient async processing for scalability
- **HTTP Server Pattern**: Production-ready deployment
- **Extensible Tools**: Easy to add new tools and integrations
- **Observable**: Full logging and debugging support

## 📄 License

Copyright (c) 2026. All rights reserved.
