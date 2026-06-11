"""
IT Ticket Management System - HTTP Server

Main entry point for the multi-agent IT ticket management system.
Uses OpenRouter AI (NVidia Nemotron 3 Super) via standard API client.
Hosts the workflow as an HTTP service via FastAPI.
"""

import os
import sys
import json
import logging
import asyncio
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Add parent directory to path so 'src' module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables first
load_dotenv(override=False)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Global workflow instance
_workflow = None


async def get_workflow():
    """Get or create the workflow instance."""
    global _workflow
    if _workflow is None:
        try:
            from src.workflow import create_workflow
            _workflow = await create_workflow()
        except ImportError as e:
            logger.error(f"Failed to import workflow: {e}")
            logger.info(f"Python path: {sys.path}")
            raise
    return _workflow


async def process_ticket_request(ticket_id: str, ticket_data: dict) -> dict:
    """
    Process a single ticket through the workflow.
    
    Args:
        ticket_id: ID of the ticket to process
        ticket_data: Ticket details
        
    Returns:
        Processing results
    """
    try:
        workflow = await get_workflow()
        result = await workflow.process_ticket(ticket_data)
        return result
    except Exception as e:
        logger.error(f"Workflow error for ticket {ticket_id}: {str(e)}", exc_info=True)
        return {
            "ticket_id": ticket_id,
            "status": "error",
            "error": f"Workflow processing failed: {str(e)[:200]}"
        }


async def create_orchestrator_agent():
    """
    Create an orchestrator agent that processes tickets.
    
    This agent serves as the main logic engine for ticket management.
    """
    # Get OpenRouter configuration
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "nemetron/nemetron-3-super")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.io/api/v1")
    
    if not api_key:
        logger.error("OPENROUTER_API_KEY environment variable not set")
        raise ValueError("OPENROUTER_API_KEY not configured")
    
    # Create client
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    logger.info(f"OpenRouter client configured with model: {model}")
    return client


async def simple_http_server():
    """
    Simple HTTP server for processing tickets (alternative to hosting adapter).
    """
    try:
        # Import FastAPI only if available
        from fastapi import FastAPI, HTTPException
        from fastapi.responses import JSONResponse
        import uvicorn
        
        app = FastAPI(
            title="IT Ticket Management System",
            description="Multi-agent system for IT ticket analysis and routing",
            version="1.0.0"
        )
        
        @app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "IT Ticket Management System"}
        
        @app.post("/tickets/process")
        async def process_ticket(ticket_data: dict):
            """
            Process an IT support ticket through the multi-agent workflow.
            
            Sample request:
            {
                "ticket_id": "INC-001",
                "title": "Password Reset Request",
                "description": "User forgot password",
                "department": "Finance",
                "affected_systems": ["Active Directory", "Email"],
                "severity_reported": "high",
                "policy_implications": ["POL-001"]
            }
            """
            try:
                result = await process_ticket_request(
                    ticket_data.get("ticket_id", "UNKNOWN"),
                    ticket_data
                )
                return result
            except Exception as e:
                logger.error(f"Error processing ticket: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        logger.info("Starting FastAPI HTTP server on 0.0.0.0:8111...")
        await uvicorn.run(
            app,
            host="0.0.0.0",
            port=8111
        )
        
    except ImportError:
        logger.warning("FastAPI not installed. Using simple async HTTP server.")
        await simple_asyncio_server()


async def simple_asyncio_server():
    """
    Fallback simple async server when FastAPI is not available.
    """
    import asyncio
    from aiohttp import web
    
    # HTML web UI
    WEB_UI = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT Ticket Management System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; color: white; margin-bottom: 40px; }
        header h1 { font-size: 2.5em; margin-bottom: 10px; }
        header p { font-size: 1.1em; opacity: 0.9; }
        .main { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .form-section, .results-section { background: white; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); padding: 30px; }
        .form-section h2, .results-section h2 { color: #667eea; margin-bottom: 20px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; color: #333; font-weight: 600; margin-bottom: 8px; }
        input, select, textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 1em; font-family: inherit; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        textarea { resize: vertical; min-height: 80px; }
        .systems-group { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
        .checkbox { display: flex; align-items: center; }
        .checkbox input { width: auto; margin-right: 8px; }
        .checkbox label { margin: 0; font-weight: normal; }
        button { background: #667eea; color: white; padding: 12px 30px; border: none; border-radius: 5px; font-size: 1em; font-weight: 600; cursor: pointer; transition: all 0.3s; }
        button:hover { background: #764ba2; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        button:disabled { background: #ccc; cursor: not-allowed; transform: none; }
        .loading { display: none; color: #667eea; text-align: center; }
        .spinner { border: 3px solid #f3f3f3; border-top: 3px solid #667eea; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .result { margin-top: 20px; padding: 20px; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 0.9em; max-height: 500px; overflow-y: auto; background: #f5f5f5; }
        .result.success { background: #e8f5e9; border-left: 4px solid #4caf50; }
        .result.error { background: #ffebee; border-left: 4px solid #f44336; }
        .result-title { font-weight: bold; color: #333; margin-bottom: 10px; }
        .policies { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
        .policy-item { display: flex; align-items: center; }
        .policy-item input { width: auto; margin-right: 8px; }
        .policy-item label { margin: 0; font-weight: normal; }
        @media (max-width: 900px) { .main { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎫 IT Ticket Management System</h1>
            <p>Multi-Agent Policy-Driven Ticket Routing</p>
        </header>
        
        <div class="main">
            <div class="form-section">
                <h2>Submit Ticket</h2>
                <form id="ticketForm">
                    <div class="form-group">
                        <label for="ticketId">Ticket ID:</label>
                        <input type="text" id="ticketId" value="INC-001" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="title">Title:</label>
                        <input type="text" id="title" placeholder="e.g., Password Reset Request" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="description">Description:</label>
                        <textarea id="description" placeholder="Describe the issue..." required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="department">Department:</label>
                        <select id="department" required>
                            <option value="">Select Department</option>
                            <option value="Finance">Finance</option>
                            <option value="Engineering">Engineering</option>
                            <option value="Sales">Sales</option>
                            <option value="Marketing">Marketing</option>
                            <option value="Operations">Operations</option>
                            <option value="HR">HR</option>
                            <option value="Security">Security</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Affected Systems:</label>
                        <div class="systems-group">
                            <div class="checkbox">
                                <input type="checkbox" id="sys1" value="Active Directory">
                                <label for="sys1">Active Directory</label>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="sys2" value="Email">
                                <label for="sys2">Email</label>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="sys3" value="VPN">
                                <label for="sys3">VPN</label>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="sys4" value="MFA">
                                <label for="sys4">MFA</label>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="sys5" value="Database">
                                <label for="sys5">Database</label>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="sys6" value="Endpoints">
                                <label for="sys6">Endpoints</label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="severity">Severity:</label>
                        <select id="severity" required>
                            <option value="">Select Severity</option>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="critical">Critical</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Policy Implications:</label>
                        <div class="policies">
                            <div class="policy-item"><input type="checkbox" value="POL-001"> <label>Password Mgmt</label></div>
                            <div class="policy-item"><input type="checkbox" value="POL-002"> <label>MFA</label></div>
                            <div class="policy-item"><input type="checkbox" value="POL-003"> <label>Data Classification</label></div>
                            <div class="policy-item"><input type="checkbox" value="POL-004"> <label>Patch Mgmt</label></div>
                            <div class="policy-item"><input type="checkbox" value="POL-005"> <label>Access Control</label></div>
                            <div class="policy-item"><input type="checkbox" value="POL-006"> <label>Device Mgmt</label></div>
                            <div class="policy-item"><input type="checkbox" value="POL-007"> <label>Incident Response</label></div>
                            <div class="policy-item"><input type="checkbox" value="POL-008"> <label>Acceptable Use</label></div>
                        </div>
                    </div>
                    
                    <button type="submit">Process Ticket</button>
                </form>
            </div>
            
            <div class="results-section">
                <h2>Analysis Results</h2>
                <div id="loadingSpinner" class="loading">
                    <div class="spinner"></div>
                    <p>Processing ticket...</p>
                </div>
                <div id="results"></div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('ticketForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Collect form data
            const systems = Array.from(document.querySelectorAll('.systems-group input[type="checkbox"]:checked')).map(cb => cb.value);
            const policies = Array.from(document.querySelectorAll('.policies input[type="checkbox"]:checked')).map(cb => cb.value);
            
            const ticketData = {
                ticket_id: document.getElementById('ticketId').value,
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                department: document.getElementById('department').value,
                affected_systems: systems,
                severity_reported: document.getElementById('severity').value,
                policy_implications: policies
            };
            
            // Show loading
            document.getElementById('loadingSpinner').style.display = 'block';
            document.getElementById('results').innerHTML = '';
            
            try {
                const response = await fetch('/tickets/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(ticketData)
                });
                
                const result = await response.json();
                
                // Hide loading
                document.getElementById('loadingSpinner').style.display = 'none';
                
                // Display result
                const resultDiv = document.createElement('div');
                resultDiv.className = 'result ' + (result.status === 'error' ? 'error' : 'success');
                
                if (result.status === 'error') {
                    resultDiv.innerHTML = `<div class="result-title">❌ Error</div><pre>${JSON.stringify(result, null, 2)}</pre>`;
                } else {
                    const riskAssessment = result.stages?.risk_assessment || {};
                    const finalAction = result.final_action || {};
                    
                    resultDiv.innerHTML = `
                        <div class="result-title">✅ Ticket Processed</div>
                        <div><strong>Ticket ID:</strong> ${result.ticket_id}</div>
                        <div><strong>Status:</strong> ${result.status}</div>
                        
                        <div style="margin-top: 20px; padding: 15px; background: #f9f9f9; border-radius: 5px;">
                            <div style="font-weight: bold; color: #667eea; margin-bottom: 10px;">🔍 Risk Assessment:</div>
                            <div><strong>Risk Score:</strong> <span style="font-size: 1.3em; color: #667eea; font-weight: bold;">${riskAssessment.risk_score || 'N/A'}/100</span></div>
                            <div><strong>Risk Level:</strong> <span style="font-weight: bold; color: ${riskAssessment.risk_level === 3 ? '#f44336' : riskAssessment.risk_level === 2 ? '#ff9800' : '#4caf50'};">Level ${riskAssessment.risk_level || 'N/A'}</span></div>
                            <div style="margin-top: 10px;"><strong>Classification:</strong> ${riskAssessment.classification || 'N/A'}</div>
                            
                            <div style="margin-top: 15px; padding: 10px; background: white; border-left: 3px solid #667eea; border-radius: 3px;">
                                <div style="font-weight: 600; color: #333; margin-bottom: 8px;">📊 AI Reasoning:</div>
                                <div style="font-size: 0.95em; line-height: 1.5; color: #555;">${riskAssessment.reasoning || 'N/A'}</div>
                            </div>
                            
                            ${riskAssessment.scoring_breakdown ? `
                            <div style="margin-top: 15px; padding: 10px; background: white; border-left: 3px solid #4caf50; border-radius: 3px;">
                                <div style="font-weight: 600; color: #333; margin-bottom: 8px;">📈 Scoring Breakdown:</div>
                                <div style="font-size: 0.9em; line-height: 1.6; color: #555;">
                                    <div>• Severity Base: <strong>${riskAssessment.scoring_breakdown.severity_base}</strong> points</div>
                                    <div>• Critical Keywords Boost: <strong>${riskAssessment.scoring_breakdown.critical_keywords_boost}</strong> points</div>
                                    <div>• System Criticality Boost: <strong>${riskAssessment.scoring_breakdown.system_criticality_boost}</strong> points</div>
                                    <div>• Policy Impact Boost: <strong>${riskAssessment.scoring_breakdown.policy_impact_boost}</strong> points</div>
                                    <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #eee;">
                                        <strong style="color: #667eea;">Final Score: ${riskAssessment.scoring_breakdown.final_score}/100</strong>
                                    </div>
                                </div>
                            </div>
                            ` : ''}
                        </div>
                        
                        <div style="margin-top: 20px;"><strong>🎯 Routing Decision:</strong></div>
                        <pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">${JSON.stringify(finalAction.routing || finalAction, null, 2)}</pre>
                    `;
                }
                
                document.getElementById('results').appendChild(resultDiv);
            } catch (error) {
                document.getElementById('loadingSpinner').style.display = 'none';
                const resultDiv = document.createElement('div');
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `<div class="result-title">❌ Connection Error</div><pre>${error.message}</pre>`;
                document.getElementById('results').appendChild(resultDiv);
            }
        });
    </script>
</body>
</html>"""
    
    async def web_ui_handler(request):
        """Serve the web UI dashboard."""
        return web.Response(text=WEB_UI, content_type='text/html')
    
    async def health_handler(request):
        """Health check endpoint."""
        response = web.json_response({
            "status": "healthy",
            "service": "IT Ticket Management System"
        })
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        return response
    
    async def process_ticket_handler(request):
        """Process ticket endpoint."""
        try:
            # Handle CORS preflight
            if request.method == 'OPTIONS':
                response = web.Response()
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
                return response
            
            # Parse JSON with error handling
            try:
                ticket_data = await request.json()
            except Exception as e:
                logger.error(f"Invalid JSON in request: {str(e)}")
                response = web.json_response(
                    {"error": f"Invalid JSON: {str(e)[:100]}"},
                    status=400
                )
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            
            # Validate ticket data
            if not ticket_data or not isinstance(ticket_data, dict):
                response = web.json_response(
                    {"error": "Request body must be a JSON object"},
                    status=400
                )
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            
            # Process ticket
            ticket_id = ticket_data.get("ticket_id", "UNKNOWN")
            logger.info(f"Processing ticket: {ticket_id}")
            
            result = await process_ticket_request(ticket_id, ticket_data)
            response = web.json_response(result)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            return response
            
        except Exception as e:
            logger.error(f"Error processing ticket: {str(e)}", exc_info=True)
            response = web.json_response(
                {"error": f"Internal server error: {str(e)[:100]}"},
                status=500
            )
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    
    # Create app
    app = web.Application()
    app.router.add_get("/", web_ui_handler)
    app.router.add_get("/health", health_handler)
    app.router.add_post("/tickets/process", process_ticket_handler)
    app.router.add_options("/tickets/process", process_ticket_handler)
    
    # Start server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8111)
    await site.start()
    
    logger.info("aiohttp server started on http://0.0.0.0:8111")
    logger.info("Endpoints:")
    logger.info("  GET / - Web UI Dashboard")
    logger.info("  GET /health - Health check")
    logger.info("  POST /tickets/process - Process a ticket")
    logger.info("")
    logger.info("🌐 Open your browser to: http://localhost:8111/")
    
    # Keep running
    try:
        await asyncio.sleep(86400)  # Run for a day
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    finally:
        await runner.cleanup()


async def main():
    """
    Main entry point - creates and runs the server.
    """
    logger.info("=" * 80)
    logger.info("IT TICKET MANAGEMENT SYSTEM - OPENROUTER VERSION")
    logger.info("=" * 80)
    
    try:
        # Verify environment setup
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or api_key.startswith("<your"):
            logger.error("❌ OPENROUTER_API_KEY not configured in .env")
            logger.error("   Please set your API key in environment: OPENROUTER_API_KEY=<your-openrouter-api-key>")
            raise ValueError("OpenRouter API key not configured")
        
        # Create orchestrator agent
        logger.info("Creating orchestrator agent...")
        agent = await create_orchestrator_agent()
        logger.info("✓ Orchestrator agent created successfully")
        
        # Start server
        logger.info("Starting HTTP server...")
        await simple_asyncio_server()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")
        logger.error("Verify:")
        logger.error("  1. OPENROUTER_API_KEY is set in .env")
        logger.error("  2. Internet connection is active")
        logger.error("  3. Dependencies installed: pip install -r requirements.txt")
        raise


if __name__ == "__main__":
    asyncio.run(main())
