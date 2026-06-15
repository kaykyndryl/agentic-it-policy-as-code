# Enhanced Features — IT Ticket Management & OPA Policy Builder

This document describes the current feature set as of June 2026, reflecting all enhancements made to both applications.

---

## 🖥️ IT Ticket Management System (Port 8111)

### Dark Developer UI

The web interface uses a fully dark theme designed for developer and operations use during extended sessions.

**Color Palette (CSS custom properties):**

| Variable | Value | Use |
|----------|-------|-----|
| `--bg-0` | `#0b1020` | Page background |
| `--bg-1` | `#121a2f` | Secondary background |
| `--card` | `#121826` | Card/panel background |
| `--line` | `#2a3550` | Borders and dividers |
| `--text-1` | `#e6ecff` | Primary text |
| `--text-2` | `#a6b3d1` | Secondary text |
| `--accent` | `#5eead4` | Teal accent / links |
| `--accent-2` | `#38bdf8` | Blue accent / highlights |
| `--ok` | `#22c55e` | Success / Level 1 green |
| `--warn` | `#f59e0b` | Warning / Level 2 amber |
| `--bad` | `#ef4444` | Danger / Level 3 red |

### One-Click Demo Scenarios

Four clickable demo buttons on the homepage auto-fill the entire ticket form (all fields including checkboxes) for instant testing:

| Button | Ticket ID | Severity | Expected Level | Domain |
|--------|-----------|----------|----------------|--------|
| 💻 Lost Laptop | INC-DEMO-001 | Critical | Level 3 — Escalate | Device / Data Security |
| 🔴 DDoS Attack | INC-DEMO-002 | Critical | Level 3 — Escalate | Infrastructure / Security |
| 👤 New Employee Onboarding | INC-DEMO-003 | Low | Level 1 — Automate | Access Provisioning |
| 🔐 VPN Access Request | INC-DEMO-004 | Medium | Level 2 — Specialist | Network Access |

Each scenario populates: Ticket ID, Title, Description, Department, Affected Systems (checkboxes), Severity radio button, and Policy Implications (checkboxes).

### Transparent Risk Scoring

The results panel displays a full **Scoring Breakdown** section alongside AI reasoning:

```
📊 Risk Score: 85/100  |  Risk Level: 3 (High)
───────────────────────────────────────────────
Scoring Breakdown:
  ⚙️  Severity Base:      60 pts   (Critical severity)
  🔑 Critical Keywords:  +20 pts  ("malware", "breach")
  🖥️  System Criticality:  +5 pts   (Database, VLAN)
  📋 Policy Impact:        0 pts   (Single policy)
```

Color-coded by factor: base score (blue), keyword boost (amber/red), system boost (teal), policy boost (purple).

### AI Reasoning Display

All three agent outputs are shown in the results panel:

1. **Policy Analysis** — TicketAnalyzerAgent: which policies apply and why
2. **Risk Assessment** — RiskAssessmentAgent: what drove the score and classification
3. **Routing Decision** — RoutingAgent: assigned team, priority, required actions

### Offline Fallback Agents

When OpenRouter API is unavailable, the system automatically uses `DemoAgents` — local rule-based implementations that:
- Produce identical service structure (scoring_factors, reasoning, final_action)
- Apply the same risk scoring logic heuristically
- Return detailed multi-part reasoning
- Require zero external dependencies

---

## 📄 OPA Policy Builder (Port 8000)

### Document Upload

Upload policy documents in **PDF** or **DOCX** format. The builder:
1. Extracts plain text from the document
2. Identifies policy-relevant sentences (keywords: must, shall, required, audit, ITAR, export, compliance)
3. Embeds matched sentences as traceability comments in the Rego output
4. Returns a downloadable `.rego` file

### 50 Auto-Generated Rego Rules

| Domain | Rules | Count |
|--------|-------|-------|
| IT Change Control | IT-001 to IT-030 | 30 |
| Manufacturing IT/OT | MFG-001 to MFG-010 | 10 |
| Government Contractor | GOV-001 to GOV-010 | 10 |

**Manufacturing IT/OT rules cover:** OT system safety, production line approvals, critical equipment, supply chain, inventory, maintenance, quality control, plant safety, ICS security, and process parameters.

**Government contractor rules cover:** ITAR export control, classified systems, foreign national access, EAR technology transfer, contract milestone notification, FISMA compliance, DoD incident response, data exfiltration controls, CUI handling, and facility access.

---

## 🔐 Security Status

| Protection | Status |
|------------|--------|
| `.env` excluded from git | ✅ `.gitignore` covers `.env`, `.env.local`, `.env.*.local` |
| `.env.template` uses placeholders only | ✅ `OPENROUTER_API_KEY=<your-openrouter-api-key>` |
| No API keys in source code | ✅ Verified — zero matches on secret patterns |
| No API keys in git history | ✅ History rewritten, force-pushed to GitHub |
| No user-specific paths in docs | ✅ All docs use generic `/path/to/` references |

---

## 🧪 Testing Scripts

| Script | Description |
|--------|-------------|
| `python test_local.py` | Offline test — loads policies, tickets, verifies tools (no API) |
| `python test_openrouter_direct.py` | Live API test — validates OpenRouter connectivity |
| `python test_comprehensive.py` | Full suite — all tools, agents, and risk levels |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | IT Ticket Management aiohttp server (port 8111), dark UI, demo scenarios |
| `src/agents.py` | OpenRouter-powered agents with scoring_factors tracking |
| `src/demo_agents.py` | Local offline fallback agents with full scoring breakdown |
| `src/workflow.py` | Multi-agent orchestration pipeline |
| `src/opa_policy_builder.py` | 50 OPA Rego rules: IT + manufacturing + government |
| `app.py` | OPA Policy Builder FastAPI app (port 8000) |
| `data/generated_policies.rego` | Last generated OPA policy output |
| `.env.template` | Configuration template — placeholder values only, safe to commit |
