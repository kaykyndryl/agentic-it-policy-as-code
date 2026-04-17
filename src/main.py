"""
IT Ticket Management System - HTTP Server

Main entry point for the multi-agent IT ticket management system.
Hosts the workflow as an HTTP service via the hosting adapter pattern.
"""

import os
import json
import logging
import asyncio
from typing import Optional
from dotenv import load_dotenv
from agent_framework import Agent, Message
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from azure.ai.agentserver.agentframework import from_agent_framework

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


async def create_agent() -> Agent:
    """
    Create the main orchestration agent.
    
    This agent serves as the HTTP endpoint for the ticket management system.
    """
    # Get Foundry configuration
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model_deployment_name = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME")
    
    if not project_endpoint or not model_deployment_name:
        logger.warning(
            "Foundry configuration not fully set. "
            "Set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL_DEPLOYMENT_NAME."
        )
        # For testing without Foundry, you could use OpenAI or other providers
        raise ValueError("Foundry configuration required")
    
    # Create Foundry client
    credential = DefaultAzureCredential()
    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model_deployment_name,
        credential=credential,
    )
    
    # Create the orchestration agent
    instructions = """You are an IT Ticket Management System orchestrator. Your role is to:

1. Accept incoming IT support tickets
2. Coordinate multi-agent analysis and processing
3. Route tickets based on risk assessment
4. Provide structured responses

When you receive a ticket request:
- Extract ticket details
- Initiate the multi-agent workflow (analysis → risk assessment → routing)
- Return comprehensive processing results including the risk level and routing decision

Format all responses as structured data with clear decision paths and reasoning."""
    
    agent = Agent(
        client=client,
        name="ITTicketOrchestrator",
        instructions=instructions
    )
    
    return agent


async def main():
    """
    Main entry point - creates and runs the HTTP server.
    """
    logger.info("Initializing IT Ticket Management System...")
    
    try:
        # Create the main agent
        agent = await create_agent()
        logger.info("Agent created successfully")
        
        # Wrap with hosting adapter and start HTTP server
        logger.info("Starting HTTP server on port 8000...")
        await from_agent_framework(agent).run_async()
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
