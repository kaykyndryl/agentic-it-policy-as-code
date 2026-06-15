# 🚀 Quick Start Guide — IT Ticket Management & OPA Policy Builder

## ✅ What This Platform Provides

Two integrated applications running on separate ports:

| App | Port | Description |
|-----|------|-------------|
| IT Ticket Management System | 8111 | Multi-agent AI ticket triage and routing |
| OPA Policy Builder | 8000 | Upload policy docs, download generated Rego rules |

### Project Structure

```
agentic-it-policy-as-code/
├── app.py                      # OPA Policy Builder (FastAPI, port 8000)
├── run_web.py                  # Startup script for OPA Policy Builder
├── src/
│   ├── main.py              # IT Ticket Management (aiohttp, port 8111)
│   ├── agents.py            # 3 AI agents via OpenRouter
│   ├── demo_agents.py       # Offline fallback agents (no API needed)
│   ├── opa_policy_builder.py # 50 OPA Rego rules (IT + manufacturing + government)
│   ├── workflow.py          # Multi-agent orchestration
│   └── tools.py             # Policy lookup, risk evaluation, routing tools
├── data/
│   ├── policies.rego        # 8 corporate IT policies
│   ├── sample_tickets.rego  # Sample tickets (all 3 risk levels)
│   └── generated_policies.rego  # Last generated OPA policy file
├── .vscode/
│   ├── launch configuration          # Debug configurations
│   └── tasks configuration           # Build/run tasks
├── .env.template            # Configuration template (placeholder values)
├── agent.yaml              # Workflow configuration
├── requirements.txt        # Python dependencies
├── test_local.py          # Local offline testing script
└── README.md              # Full documentation
```

### What's Changed

Your system now uses **OpenRouter AI** instead of Azure Foundry:

| Component | Before | Now |
|-----------|--------|-----|
| AI Client | `FoundryChatClient` | `AsyncOpenAI` (OpenRouter API client) |
| Authentication | Azure credentials | OpenRouter API key |
| API Endpoint | Azure AI Foundry | OpenRouter (`openrouter.io/api/v1`) |
| Setup Complexity | Complex Foundry setup | Free OpenRouter account |
| Cost | Azure compute + models | Pay-as-you-go (free tier available) |

### Quick Start Steps

#### Step 1: Get OpenRouter API Key (2 minutes)

1. Go to https://openrouter.ai
2. Sign up (free)
3. Copy your API key from settings
4. Create `.env` from the template: `cp .env.template .env`
5. Edit `.env` and paste your key as `OPENROUTER_API_KEY=<your-openrouter-api-key>`

> **Security note:** Never commit `.env`. It is excluded by `.gitignore`. Only `.env.template` with placeholder values is tracked in git.

#### Step 2: Install Dependencies (2 minutes)

```bash
cd /path/to/agentic-it-policy-as-code
pip install -r requirements.txt
```

#### Step 3: Run Local Test (1 minute)

```bash
python test_local.py
```

Output:
```
IT TICKET MANAGEMENT SYSTEM - LOCAL TEST
================================================================================
📊 Loaded 7 sample tickets
📋 Loaded 8 IT policies

--- SAMPLE TICKETS ---
TICKET: TKT-001 - Password Reset Request
Department: Finance
Severity: high
Systems: Active Directory, Email
Expected Risk Level: 1

--- SAMPLE POLICIES ---
📋 POL-001: Password Security Policy
   Category: password_management
   Scope: mandatory
   Key Reqs: 4 requirements
...
✅ LOCAL TEST COMPLETE
```

#### Step 4: Start Both Services

**IT Ticket Management System** (open one terminal):
```bash
python -m src.main
```
Web UI available at: `http://localhost:8111`

Click any of the four **Quick Demo** buttons to auto-fill a scenario and hit **Process Ticket**.

**OPA Policy Builder** (open a second terminal):
```bash
python run_web.py
```
Available at: `http://localhost:8000`

Upload a policy PDF or DOCX to generate downloadable Rego change-control rules.

#### Step 5: Test with a Ticket via API

In another terminal:

```bash
curl -X POST http://localhost:8111/tickets/process \
    -d '{
    "ticket_id": "TKT-002",
    "title": "Cannot Access VPN",
    "description": "VPN connection fails",
    "department": "Engineering",
    "affected_systems": ["VPN", "MFA"],
    "severity_reported": "critical",
    "policy_implications": ["POL-002"]
  }'
```

Response:
```text
{
  "ticket_id": "TKT-002",
  "status": "completed",
  "final_action": {
    "risk_level": 2,
    "classification": "Level 2 - Medium Risk",
    "routing": {
      "assigned_team": "Security Operations",
      "priority": "high",
      "escalation_required": false
    }
  }
}
```

## 📋 Configuration

Copy the template and add your API key:

```bash
cp .env.template .env
```

Edit `.env`:

```env
OPENROUTER_API_KEY=<your-openrouter-api-key>
OPENROUTER_MODEL=nemetron/nemetron-3-super
OPENROUTER_BASE_URL=https://openrouter.io/api/v1
LOG_LEVEL=INFO
DEBUG_MODE=false
```

> **Security:** `.env` is git-ignored. Only `.env.template` (with placeholder values) is committed to the repository. Never put a real API key in `.env.template`.

## 🎯 How It Works

### Architecture

```
Incoming Ticket (rego-backed payload)
        ↓
   [HTTP Server]
        ↓
[TicketAnalyzerAgent] (OpenRouter)
   ├─ Extract info
   ├─ Check policies
   └─ Returns: Analysis
        ↓
[RiskAssessmentAgent] (OpenRouter)
   ├─ Evaluate severity
   ├─ Compute risk score
   └─ Returns: Level 1/2/3
        ↓
[RoutingAgent] (OpenRouter)
   ├─ Level 1? → Automate
   ├─ Level 2-3? → Route to team
   └─ Returns: Action plan
        ↓
   Response (service output)
```

### Example Flows

**Level 1 Ticket (Auto):**
```
Request: "Password Reset"
         ↓
Analysis: "Common issue, POL-001"
         ↓
Risk: Score=15, Level=1 (Low)
         ↓
Action: Auto-remediate (send reset link)
```

**Level 3 Ticket (Escalate):**
```
Request: "Suspicious email with attachment"
         ↓
Analysis: "Potential malware, POL-007 Incident Response"
         ↓
Risk: Score=95, Level=3 (Critical)
         ↓
Action: Escalate to SOC immediately
```

## 🧪 Tests Available

### Test Local (No API calls)

```bash
python test_local.py
```

Tests:
- ✅ Policies load (8 loaded)
- ✅ Tickets load (7 loaded)
- ✅ Tool functions work

### Manual API Test

```bash
# Health check (ticket service)
curl http://localhost:8111/health

# Process ticket via API
curl -X POST http://localhost:8111/tickets/process \
   -d @sample_ticket.rego
```

## 📊 Core Components

### Agents (Using OpenRouter)

1. **TicketAnalyzerAgent**
   - Analyzes tickets against IT policies
   - Identifies policy implications
   - Returns structured analysis

2. **RiskAssessmentAgent**
   - Calculates risk scores (0-100)  
   - Assigns levels 1/2/3
   - Provides reasoning

3. **RoutingAgent**
   - For Level 1: Provides automation steps
   - For Level 2-3: Routes to support teams
   - Determines priority and escalation

### Policies (Configurable)

8 IT policies in `data/policies.rego`:
- POL-001: Password Management
- POL-002: Multi-Factor Authentication
- POL-003: Data Classification & Handling
- POL-004: Patch Management
- POL-005: Access Control
- POL-006: Device Management
- POL-007: Incident Response
- POL-008: Acceptable Use

### Tools (Local)

5 tools in `src/tools.py`:
- PolicyLookupTool
- TicketDatabaseTool
- RiskEvaluationTool
- RemediationTool
- NotificationTool

## 🔧 Debug Configurations

**F5 to Debug** - Choose configuration:

1. **Run Local Test**
   - Tests all components
   - No OpenRouter API calls
   - Fast feedback

2. **Run Main Server**
   - Starts HTTP server
   - Ready for requests
   - Real-time processing

## 📞 Next Steps

### Immediate (5 mins)
- [ ] Run `python test_local.py`
- [ ] Start server: `python -m src.main`
- [ ] Test with curl

### Short Term (30 mins)
- [ ] Customize policies in `data/policies.rego`
- [ ] Add real sample tickets in `data/sample_tickets.rego`
- [ ] Test with your IT tickets
- [ ] Debug with VS Code (F5)

### Production (Later)
- [ ] Deploy to Azure Container Apps or App Service
- [ ] Integrate with ServiceNow/Jira
- [ ] Set up automated ticket ingestion
- [ ] Monitor with Application Insights

## 🆘 Troubleshooting

### "OPENROUTER_API_KEY not configured"
```
✓ Fix: Check .env file has your API key
$ cat .env | grep OPENROUTER_API_KEY
```

### "Connection refused" on localhost:8111
```
✓ Fix: Start the ticket management server:
$ python -m src.main

For OPA Policy Builder (port 8000):
$ python run_web.py
```

### "Rate limit exceeded"
```
✓ OpenRouter has usage limits for free tier
✓ Upgrade account or wait before retry
```

### "Model not available"
```
✓ Check available models: https://openrouter.io/models
✓ Update OPENROUTER_MODEL in .env
```

## 📚 Documentation

- **README.md** - Full architecture and API reference
- **DEMO_test_local.md** - Detailed walkthrough of demo script
- **QUICKSTART.md** - This file

---

**System is ready to use! Start with:** `python test_local.py` ✅
- All 5 tools verified working
- Risk assessment functional
- Routing logic operational

---

## 🔧 Environment Status

**Python Environment:**
- Type: Virtual Environment (venv)
- Location: `./venv/`
- Python Version: 3.11.15 ✓
- All dependencies installed ✓

**Installed Packages:**
- agent-framework-core==1.0.0rc6 ✓
- agent-framework-foundry==1.0.0rc6 ✓
- agent-framework-openai==1.0.0rc6 ✓ (Replaced by standard API client)
- azure-ai-agentserver-agentframework==1.0.0b16 ✓
- azure-ai-agentserver-core==1.0.0b16 ✓
- agent-dev-cli==0.0.1b260316 ✓
- azure-identity ✓
- python-dotenv ✓

---

## 📋 Next Steps

- [ ] Open `http://localhost:8111` in a browser and try the four demo scenarios
- [ ] Open `http://localhost:8000` and upload a PDF/DOCX policy document to generate OPA Rego rules
- [ ] Customize policies in `data/policies.rego`
- [ ] Adjust risk thresholds in `src/demo_agents.py`
- [ ] Add new demo scenarios in the `DEMO_TICKETS` dict inside `src/main.py`
- [ ] Review `README.md` for full architecture and API reference

---

**System is ready!**
- `python -m src.main` → IT Ticket Management at `http://localhost:8111` ✅
- `python run_web.py` → OPA Policy Builder at `http://localhost:8000` ✅

# Option 2: Azure CLI
az containerapp up --name it-ticket-management \
  --resource-group <rg> \
  --ingress external \
  --target-port 8000
```

---

## 🧪 Testing the System

### Test Ticket Scenarios

The system includes 7 sample tickets demonstrating all risk levels:

**Level 1 (Low Risk - Automated):**
- TKT-001: Password Reset Request (5-10 min auto fix)
- TKT-004: Monitor Connection Issues (hardware troubleshooting)
- TKT-006: Printer Driver Installation

**Level 2 (Medium Risk - Specialist Review):**
- TKT-002: VPN/MFA Access Issues
- TKT-007: Database Access Request

**Level 3 (High Risk - Escalation):**
- TKT-003: Suspicious Email/Malware
- TKT-005: Unauthorized File Share Exposure

### View or Add Tickets

Sample tickets are in `data/sample_tickets.rego`. To add new tickets:

```text
{
  "ticket_id": "TKT-008",
  "title": "Your ticket title",
  "description": "Description",
  "department": "Department",
  "severity_reported": "low|medium|high|critical",
  "affected_systems": ["System1", "System2"],
  "policy_implications": ["POL-001", "POL-002"]
}
```

### Customize Policies

Edit `data/policies.rego` to add your organization's policies:

```text
{
  "id": "POL-009",
  "category": "custom_category",
  "title": "Your Policy Title",
  "description": "Description",
  "key_requirements": ["Requirement 1", "Requirement 2"],
  "compliance_level": "mandatory",
  "enforcement": "Enforcement method"
}
```

---

## 🎯 Development Workflow

### VS Code Tasks (Ctrl+Shift+B)

```
Install Dependencies    → Run first time to verify setup
Run Local Test         → Test all tools and components
Start HTTP Server      → Run production server
Format Code            → Black formatter
Lint Code              → Code quality check
```

### Debug Configurations (F5)

**Run Main Server** (default)
- Starts HTTP server with debugging
- Breakpoints work
- Console shows logs

**Run Local Test**
- Verifies all tools
- Tests sample data
- No need for Foundry credentials

**Debug with AI Toolkit Inspector**
- Interactive agent tracing
- Message flow visualization
- Tool call inspection

---

## 🔐 Security Notes

### For Development
- ✅ All credentials in `.env` (local only)
- ✅ `.gitignore` prevents accidental commits
- ✅ Test uses sample data only

### For Production Deployment
- [ ] Use Azure Managed Identity instead of credentials
- [ ] Enable Application Insights for monitoring
- [ ] Configure HTTPS/TLS
- [ ] Implement authentication on HTTP endpoints
- [ ] Set up audit logging for ticket access
- [ ] Use Azure Key Vault for secrets
- [ ] Review and customize access controls

---

## 🚀 Going to Production

### Deployment Checklist

- [ ] Update `.env` with Foundry credentials
- [ ] Run `python test_local.py` successfully
- [ ] Test with F5 debug mode
- [ ] Review and customize policies for your org
- [ ] Add your actual ticketing system integration
- [ ] Configure team notifications (email, Azure DevOps, Slack)
- [ ] Set up monitoring/alerts with Application Insights
- [ ] Deploy using Microsoft Foundry
- [ ] Test end-to-end workflow

### Performance Tuning

- Multi-agent processing: ~2-5 seconds per ticket
- Risk assessment: Real-time policy checks
- Scalability: Async processing supports concurrent tickets
- Cost: Depends on model size and token usage

---

## 📚 Key Files to Review

1. **README.md** - Complete architecture and deployment guide
2. **src/main.py** - HTTP server entry point
3. **src/agents.py** - Agent definitions and instructions
4. **src/workflow.py** - Multi-agent orchestration logic
5. **src/tools.py** - All tool implementations
6. **data/policies.rego** - Corporate policies
7. **.vscode/launch configuration** - Debug configurations

---

## 💡 Extension Ideas

Your system is built to be extended:

1. **Real Ticketing System Integration**
   - ServiceNow connector
   - Jira API integration
   - GitHub Issues support

2. **Enhanced Tools**
   - Active Directory/Entra ID integration
   - Email notification system
   - Slack/Teams notifications
   - Dashboard for metrics

3. **Advanced Features**
   - Machine learning for risk scoring refinement
   - Ticket categorization improvements
   - Historical analytics
   - Approval workflows

4. **Multi-Language Support**
   - French, Spanish, German policies
   - Localized ticket processing

---

## 🆘 Troubleshooting

### Issue: "Foundry configuration not set"
**Solution:** Update `.env` with your Foundry project details

### Issue: "Agent failed to respond"
**Solution:** Check internet connection and Foundry endpoint availability

### Issue: "Import errors"
**Solution:** Run `pip install -r requirements.txt` to ensure all dependencies are installed

### Issue: "Debug not working"
**Solution:** Make sure Python extension is installed in VS Code

---

## 📞 Support Resources

- **Agent Framework Docs**: https://github.com/microsoft/agent-framework
- **Azure AI Foundry**: https://www.microsoft.com/en-us/cloud-platform/azure-ai-foundry
- **Python Issues**: Check terminal output and `.vscode/launch configuration`

---

## ✨ You're All Set!

Your intelligent IT ticket management system is ready for:
- ✅ Local development and testing
- ✅ Interactive debugging with F5
- ✅ Production deployment to Azure Foundry
- ✅ Customization with your policies and integrations

**Recommended Next Action:** Press F5 to start the HTTP server and verify everything is working!

---

*Created: April 16, 2026*
*Agent Framework: 1.0.0rc6*
*Python: 3.11.15*
