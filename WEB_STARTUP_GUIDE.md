# 🚀 Starting the Web-Based IT Ticket Management System

This guide will help you start the solution as a web-based application.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the template environment file:
```bash
cp .env.template .env
```

Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-4-turbo
OPENROUTER_BASE_URL=https://openrouter.io/api/v1
```

### 3. Start the Web Server

**Option A: Using the startup script (Recommended)**
```bash
python run_web.py
```

**Option B: Using uvicorn directly**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Option C: Using Python**
```bash
python -m app
```

### 4. Access the Web Interface

Once the server is running, open your browser and visit:
```
http://localhost:8000
```

You should see the IT Ticket Management System interface.

## Features

### 🎫 Submit Tickets
- Fill out the ticket form with issue details
- Select severity level
- Specify affected systems and departments
- Submit for analysis

### 📊 Real-Time Analysis
The system performs:
1. **Policy Analysis** - Analyzes tickets against corporate IT policies
2. **Risk Assessment** - Evaluates severity and compliance risk
3. **Intelligent Routing** - Routes to appropriate teams or auto-remediation

### 🎯 Quick Examples
Try the pre-loaded sample tickets:
- 🔐 Password Reset Request
- 🔒 VPN/MFA Access Issue
- ⚠️ Security Alert/Malware

## API Endpoints

### Web Interface
- `GET /` - Main web interface

### API Documentation
- `GET /api/docs` - Interactive API documentation (Swagger UI)
- `GET /api/redoc` - Alternative API documentation (ReDoc)

### Core Endpoints
- `GET /api/health` - Health check
- `POST /api/tickets/process` - Process a single ticket
- `POST /api/tickets/batch` - Process multiple tickets
- `GET /api/policies` - Get all IT policies
- `GET /api/policies/{policy_id}` - Get specific policy
- `GET /api/sample-tickets` - Get sample tickets

### Request/Response Example

**Request:**
```json
POST /api/tickets/process
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
```json
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
WEB_HOST=0.0.0.0          # Server host (default: 0.0.0.0)
WEB_PORT=8000             # Server port (default: 8000)
ENVIRONMENT=development   # Set to 'development' for auto-reload
LOG_LEVEL=info           # Logging level: debug, info, warning, error, critical

# AI Configuration
OPENROUTER_API_KEY=sk-...          # Required: OpenRouter API key
OPENROUTER_MODEL=openai/gpt-4-turbo # Model to use
OPENROUTER_BASE_URL=https://openrouter.io/api/v1  # API endpoint
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```bash
python run_web.py --port 8080
```

### Module Not Found Error
Make sure you're in the correct directory and dependencies are installed:
```bash
cd /Users/kayapperson/Documents/agentic-it-policy-as-code/agentic-it-policy-as-code
pip install -r requirements.txt
python run_web.py
```

### API Key Error
Ensure your `.env` file has a valid OPENROUTER_API_KEY:
```bash
cat .env | grep OPENROUTER_API_KEY
```

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
┌─────────────────────────────────────────────────┐
│         Web Browser / Client                     │
│  (HTML Interface at http://localhost:8000)      │
└──────────────────┬──────────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────────┐
│         FastAPI Web Server (app.py)             │
│  - Routes requests to API endpoints             │
│  - Serves HTML frontend                         │
│  - Manages CORS and responses                   │
└──────────────────┬──────────────────────────────┘
                   │ Python Async
┌──────────────────▼──────────────────────────────┐
│      Multi-Agent Workflow (src/workflow.py)     │
│  - TicketAnalyzerAgent                          │
│  - RiskAssessmentAgent                          │
│  - RoutingAgent                                 │
└──────────────────┬──────────────────────────────┘
                   │ API Calls
┌──────────────────▼──────────────────────────────┐
│         OpenRouter AI Service                   │
│  (OpenAI-compatible endpoint)                   │
└─────────────────────────────────────────────────┘
```

---

**Need help?** Check the main README.md or review the API documentation at `/api/docs`
