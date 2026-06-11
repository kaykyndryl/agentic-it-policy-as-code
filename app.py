"""
IT Ticket Management System - Web Application

FastAPI web server for the multi-agent IT ticket management system.
Provides REST API endpoints and serves the web interface.
"""

import os
import json
import logging
import re
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from src.opa_policy_builder import (
    POLICY_RULES,
    build_rego_policy,
    extract_policy_candidates,
    extract_text_from_document,
)

# Load environment variables
load_dotenv(override=False)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="IT Ticket Management System",
    description="Multi-agent system for IT ticket analysis and routing",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global workflow instance
_workflow = None


# Request/Response Models
class TicketRequest(BaseModel):
    """Ticket submission request model."""
    ticket_id: Optional[str] = None
    title: str
    description: str
    department: str
    affected_systems: list[str] = []
    severity_reported: str = "medium"
    urgency: str = "medium"
    policy_implications: list[str] = []


class TicketResponse(BaseModel):
    """Ticket processing response model."""
    ticket_id: str
    timestamp: str
    status: str
    stages: dict = {}
    error: Optional[str] = None


# Utility Functions
async def get_workflow():
    """Get or create the workflow instance."""
    global _workflow
    if _workflow is None:
        logger.info("Initializing workflow...")
        from src.workflow import create_workflow
        _workflow = await create_workflow()
        logger.info("Workflow initialized successfully")
    return _workflow


def load_policies():
    """Load policies from data file."""
    try:
        policies_file = Path(__file__).parent / "data" / "policies.json"
        if policies_file.exists():
            with open(policies_file, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading policies: {e}")
    return {"policies": []}


def load_sample_tickets():
    """Load sample tickets from data file."""
    try:
        tickets_file = Path(__file__).parent / "data" / "sample_tickets.json"
        if tickets_file.exists():
            with open(tickets_file, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading sample tickets: {e}")
    return {"tickets": []}


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML interface."""
    html_file = Path(__file__).parent / "web_demo.html"
    if html_file.exists():
        return html_file.read_text()
    return "<h1>IT Ticket Management System</h1><p>Loading...</p>"


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "IT Ticket Management System",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/api/policies")
async def get_policies():
    """Get all IT policies."""
    policies = load_policies()
    return {
        "status": "success",
        "count": len(policies.get("policies", [])),
        "policies": policies.get("policies", [])
    }


@app.get("/api/policies/{policy_id}")
async def get_policy(policy_id: str):
    """Get a specific policy by ID."""
    policies = load_policies()
    for policy in policies.get("policies", []):
        if policy.get("id") == policy_id:
            return {"status": "success", "policy": policy}
    raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")


@app.get("/api/sample-tickets")
async def get_sample_tickets():
    """Get sample tickets for testing."""
    tickets = load_sample_tickets()
    return {
        "status": "success",
        "count": len(tickets.get("tickets", [])),
        "tickets": tickets.get("tickets", [])
    }


@app.post("/api/tickets/process", response_model=TicketResponse)
async def process_ticket(ticket_request: TicketRequest):
    """
    Process an IT support ticket through the multi-agent workflow.
    
    This endpoint:
    1. Analyzes the ticket against policies
    2. Assesses risk level
    3. Routes to appropriate team
    
    Example request:
    {
        "title": "Password Reset Request",
        "description": "User forgot password",
        "department": "Finance",
        "affected_systems": ["Active Directory", "Email"],
        "severity_reported": "high",
        "policy_implications": ["POL-001"]
    }
    """
    try:
        # Prepare ticket data
        ticket_data = ticket_request.model_dump()
        
        # Generate ticket ID if not provided
        if not ticket_data.get("ticket_id"):
            ticket_data["ticket_id"] = f"INC-{int(datetime.now().timestamp())}"
        
        ticket_id = ticket_data["ticket_id"]
        logger.info(f"Processing ticket {ticket_id}: {ticket_data.get('title')}")
        
        # Get workflow and process ticket
        workflow = await get_workflow()
        result = await workflow.process_ticket(ticket_data)
        
        logger.info(f"Ticket {ticket_id} processed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error processing ticket: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process ticket: {str(e)[:200]}"
        )


@app.get("/api/tickets/{ticket_id}")
async def get_ticket_status(ticket_id: str):
    """Get status of a processed ticket (placeholder for future enhancement)."""
    return {
        "status": "info",
        "ticket_id": ticket_id,
        "message": "Ticket tracking feature coming soon"
    }


@app.post("/api/tickets/{ticket_id}/override-severity")
async def override_severity(ticket_id: str, override_severity: dict):
    """
    Handle human-in-the-loop severity override.
    
    Allows IT support agent to override AI-recommended or user-reported severity.
    
    Request body:
    {
        "user_reported_severity": "low",
        "ai_recommended_severity": "high", 
        "confirmed_severity": "high",
        "reasoning": "Based on email pattern analysis..."
    }
    """
    try:
        logger.info(f"Severity override for {ticket_id}: {override_severity.get('confirmed_severity')}")
        return {
            "status": "override_confirmed",
            "ticket_id": ticket_id,
            "original_severity": override_severity.get("user_reported_severity"),
            "ai_recommended": override_severity.get("ai_recommended_severity"),
            "confirmed_severity": override_severity.get("confirmed_severity"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error processing severity override: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/tickets/batch")
async def batch_process_tickets(tickets: list[TicketRequest]):
    """
    Process multiple tickets in batch.
    
    Useful for testing with multiple sample tickets.
    """
    results = []
    for ticket_request in tickets:
        try:
            result = await process_ticket(ticket_request)
            results.append(result)
        except Exception as e:
            results.append({
                "ticket_id": ticket_request.ticket_id or "UNKNOWN",
                "status": "error",
                "error": str(e)
            })
    
    return {
        "status": "completed",
        "total_processed": len(tickets),
        "successful": len([r for r in results if r.get("status") != "error"]),
        "failed": len([r for r in results if r.get("status") == "error"]),
        "results": results
    }


@app.post("/api/opa/generate-from-document")
async def generate_opa_from_document(file: UploadFile = File(...)):
    """Generate OPA Rego policy code from an uploaded PDF/DOCX/DOC document."""
    try:
        filename = file.filename or "uploaded_policy_document"
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        raw_text = extract_text_from_document(filename, content)
        cleaned_text = re.sub(r"\s+", " ", raw_text).strip()
        extracted = extract_policy_candidates(cleaned_text, limit=12)
        rego_content = build_rego_policy(filename, extracted)

        output_path = Path(__file__).parent / "data" / "generated_policies.rego"
        output_path.write_text(rego_content, encoding="utf-8")

        return {
            "status": "success",
            "document": filename,
            "extracted_policy_candidates": extracted,
            "policy_count": len(POLICY_RULES),
            "rego_file": str(output_path),
            "rego": rego_content,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Failed to generate OPA policies: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate OPA policies") from exc


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Custom general exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("WEB_HOST", "0.0.0.0")
    port = int(os.getenv("WEB_PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    logger.info(f"Starting IT Ticket Management System on {host}:{port}")
    logger.info("Open your browser to http://localhost:8000")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT", "development") == "development",
        log_level=log_level
    )
