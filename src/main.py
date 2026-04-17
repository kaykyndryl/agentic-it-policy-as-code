"""
IT Ticket Management System - HTTP Server

Main entry point for the multi-agent IT ticket management system.
Uses OpenRouter AI (OpenAI-compatible API) for agent execution.
Hosts the workflow as an HTTP service via FastAPI.
"""

import os
import json
import logging
import asyncio
from typing import Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI

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
        from src.workflow import create_workflow
        _workflow = await create_workflow()
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
    workflow = await get_workflow()
    result = await workflow.process_ticket(ticket_data)
    return result


async def create_orchestrator_agent():
    """
    Create an orchestrator agent that processes tickets.
    
    This agent serves as the main logic engine for ticket management.
    """
    # Get OpenRouter configuration
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4-turbo")
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
                "ticket_id": "TKT-001",
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
        
        logger.info("Starting FastAPI HTTP server on 0.0.0.0:8000...")
        await uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000
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
    
    async def health_handler(request):
        """Health check endpoint."""
        return web.json_response({
            "status": "healthy",
            "service": "IT Ticket Management System"
        })
    
    async def process_ticket_handler(request):
        """Process ticket endpoint."""
        try:
            ticket_data = await request.json()
            result = await process_ticket_request(
                ticket_data.get("ticket_id", "UNKNOWN"),
                ticket_data
            )
            return web.json_response(result)
        except Exception as e:
            logger.error(f"Error processing ticket: {str(e)}")
            return web.json_response(
                {"error": str(e)},
                status=500
            )
    
    # Create app
    app = web.Application()
    app.router.add_get("/health", health_handler)
    app.router.add_post("/tickets/process", process_ticket_handler)
    
    # Start server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    
    logger.info("aiohttp server started on http://0.0.0.0:8000")
    logger.info("Endpoints:")
    logger.info("  GET /health - Health check")
    logger.info("  POST /tickets/process - Process a ticket")
    
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
        # Create orchestrator agent
        agent = await create_orchestrator_agent()
        logger.info("✓ Orchestrator agent created successfully")
        
        # Start server
        logger.info("Starting HTTP server...")
        await simple_asyncio_server()
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
