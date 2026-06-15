# 🚀 Starting Both Web Services

This project runs as **two separate applications** on different ports:

| Service | Port | Description |
|---------|------|-------------|
| IT Ticket Management System | 8111 | Multi-agent AI ticket analysis and routing |
| OPA Policy Builder | 8000 | Upload policy docs, generate OPA Rego rules |

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the template:
```bash
cp .env.template .env
```

Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=<your-openrouter-api-key>
OPENROUTER_MODEL=nemetron/nemetron-3-super
OPENROUTER_BASE_URL=https://openrouter.io/api/v1
```

> **Security:** `.env` is excluded from git by `.gitignore`. Never put a real key in `.env.template`.

### 3. Start IT Ticket Management System (Port 8111)

```bash
python -m src.main
```

Open in browser: `http://localhost:8111`

The UI features:
- **Dark developer theme** with high-contrast colors optimized for extended use
- **Four quick-demo buttons** that auto-fill the form with realistic scenarios
- **Risk score breakdown** showing base score + keyword boost + system boost + policy boost
- **Detailed AI reasoning** from all three agents displayed in results

### 4. Start OPA Policy Builder (Port 8000)

**Option A: Using the startup script (Recommended)**
```bash
python run_web.py
```

**Option B: Using uvicorn directly**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Open in browser: `http://localhost:8000`

The OPA Policy Builder allows you to:
- Upload a PDF or DOCX policy document
- Auto-extract policy-relevant sentences
- Download a complete `.rego` file with 50 deny rules covering:
  - 30 IT Change Control rules (IT-001 to IT-030)
  - 10 Manufacturing IT/OT rules (MFG-001 to MFG-010)
  - 10 Government Contractor rules (GOV-001 to GOV-010, covering ITAR, FISMA, CUI)

## Features

### 🎫 IT Ticket Management (Port 8111)
- **Dark UI** — developer-friendly dark theme with CSS custom properties
- **One-Click Demo Scenarios:**
  - 💻 Lost Laptop — remote worker device security incident (Critical, Level 3)
  - 🔴 DDoS Attack — Linux production server under attack (Critical, Level 3)
  - 👤 New Employee Onboarding — access provisioning request (Low, Level 1)
  - 🔐 VPN Access Request — network access for remote work (Medium, Level 2)
- **Submit Tickets** — fill out form or click a demo to auto-fill all fields
- **Real-Time AI Analysis** — policy analysis, risk scoring, and routing in one pass
- **Scoring Transparency** — see every factor contributing to the final risk score

### 📄 OPA Policy Builder (Port 8000)
- **Upload Policy Documents** — accepts PDF and DOCX files
- **Auto-Extract Statements** — identifies policy-relevant sentences using keyword matching
- **Generate Rego Rules** — produces 50 deterministic OPA deny rules
- **Download .rego Files** — ready for deployment to your OPA instance
- **Domains Covered:** IT Change Control, Manufacturing OT/IT, Government Contractor (ITAR, FISMA, CUI)

## API Endpoints

### IT Ticket Management (Port 8111)

- `POST /tickets/process` — Submit and process a single ticket
- `GET /health` — Health check

### OPA Policy Builder (Port 8000)

- `GET /` — Web interface
- `GET /api/docs` — Interactive API documentation (Swagger UI)
- `GET /api/redoc` — Alternative documentation (ReDoc)
- `GET /api/health` — Health check
- `POST /api/opa/generate-from-document` — Upload document, get generated Rego policy
- `GET /api/policies` — List all built-in IT policies
- `GET /api/policies/{policy_id}` — Get a specific policy
- `GET /api/sample-tickets` — List sample tickets

### Request/Response Example — IT Ticket Management

**Request:**
```text
POST http://localhost:8111/tickets/process
{
  "title": "Password Reset Request",
  "description": "User forgot their password",
  "department": "Finance",
  "affected_systems": ["Active Directory", "Email"],
  "severity_reported": "high",
  "policy_implications": ["POL-001"]
}
```

**Response:**
```text
{
  "ticket_id": "TKT-1234567890",
  "timestamp": "2026-04-17T12:34:56.789000",
  "status": "processing",
  "stages": {
    "analysis": {
      "status": "completed",
      "content": "..."
    },
    "risk_assessment": {
      "status": "completed",
      "risk_level": 1,
      "risk_score": 25
    },
    "routing": {
      "status": "completed",
      "routing_decision": "..."
    }
  }
}
```

## Configuration Options

### Environment Variables

```bash
# Server Configuration
WEB_HOST=0.0.0.0          # OPA Policy Builder host (default: 0.0.0.0)
WEB_PORT=8000             # OPA Policy Builder port (default: 8000)
ENVIRONMENT=development   # Set to 'development' for auto-reload
LOG_LEVEL=info           # Logging level: debug, info, warning, error, critical

# AI Configuration
OPENROUTER_API_KEY=<your-openrouter-api-key>  # Required: OpenRouter API key
OPENROUTER_MODEL=nemetron/nemetron-3-super    # NVidia Nemotron 3 Super
OPENROUTER_BASE_URL=https://openrouter.io/api/v1
```

> The IT Ticket Management System runs on port 8111 and is configured directly in `src/main.py`.

## Troubleshooting

### Port Already in Use
```bash
# Kill whatever is using port 8000
lsof -i :8000 | awk 'NR>1{print $2}' | xargs kill -9
python run_web.py

# Kill whatever is using port 8111
lsof -i :8111 | awk 'NR>1{print $2}' | xargs kill -9
python -m src.main
```

### Module Not Found Error
```bash
cd /path/to/agentic-it-policy-as-code
pip install -r requirements.txt
```

### API Key Error
Ensure your `.env` file has a valid `OPENROUTER_API_KEY`:
```bash
cat .env | grep OPENROUTER_API_KEY
```
If the key is missing or invalid, the ticket management system falls back to local demo agents automatically — all UI functionality still works.

### CORS/Connection Errors
Make sure the server is running on the correct host/port:
```bash
# Check what's running on port 8000
lsof -i :8000
```

## Performance Tips

### Auto-Reload
The server runs in development mode with auto-reload by default. This means the server will restart when you modify Python files. For production:
```bash
python run_web.py --reload=false
```

### Logging
Adjust log level for better performance:
```bash
python run_web.py --log-level warning
```

## Next Steps

- Explore the API documentation at `/api/docs`
- Try submitting tickets with different severity levels
- Review the analysis and routing decisions
- Integrate with your IT ticketing system

## Architecture

```
┌──────────────────────────────────────────────────────┐
│              Web Browser / Client                    │
│  Port 8111: IT Ticket System (dark theme UI)        │
│  Port 8000: OPA Policy Builder (Swagger UI)         │
└──────────────────────────────────────────────────────┘
       │ HTTP (8111)                 │ HTTP (8000)
┌──────┴──────────────────┐  ┌──────┴──────────────────┐
│  aiohttp (src/main.py)  │  │  FastAPI (app.py)        │
│  IT Ticket Management   │  │  OPA Policy Builder      │
│  Port 8111              │  │  Port 8000               │
└──────┬──────────────────┘  └──────┬──────────────────┘
       │ Python async               │ OPA Rego generation
┌──────┴──────────────────┐  ┌──────┴──────────────────┐
│  Multi-Agent Workflow   │  │  opa_policy_builder.py  │
│  Analyzer→Risk→Router   │  │  50 deny rules:         │
│  (src/workflow.py)      │  │  IT + MFG + GOV         │
└──────┬──────────────────┘  └─────────────────────────┘
       │
┌──────┴──────────────────┐
│  OpenRouter AI Service  │
│  NVidia Nemotron 3 Super│
│  (auto-falls back to    │
│   demo agents offline)  │
└─────────────────────────┘
```

---

**Need help?** Check the main README.md or browse the OPA Policy Builder API at `http://localhost:8000/api/docs`
