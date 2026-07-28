"""
Project Munde — FastAPI Backend
Single unified API endpoint for the agentic AI platform.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from munde.runtime.orchestrator import orchestrator
from munde.runtime.agent_registry import registry
import structlog

logger = structlog.get_logger(__name__)

# Auto-load domain packs on startup
import munde.domain_packs.sahyadri.register  # This triggers registration

app = FastAPI(
    title="Project Munde",
    description="Agentic AI Platform — General-purpose multi-agent orchestration",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "anonymous"
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    response: Dict[str, Any]
    platform_info: Dict[str, Any]

@app.post("/api/v1/ask")
async def ask_munde(request: QueryRequest) -> QueryResponse:
    """
    Unified endpoint for all queries.
    The orchestrator routes to the appropriate agent(s).
    """
    logger.info("query_received", query=request.query[:100], user_id=request.user_id)
    
    try:
        response = await orchestrator.process_query(request.query, request.context)
        
        return QueryResponse(
            response=response.dict(),
            platform_info={
                "registered_agents": registry.list_agents(),
                "available_capabilities": registry.list_capabilities(),
            }
        )
    except Exception as e:
        logger.error("query_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/agents")
async def list_agents():
    """List all registered agents"""
    agents = []
    for name in registry.list_agents():
        info = registry.get_agent_info(name)
        if info:
            agents.append(info)
    return {"agents": agents}

@app.get("/api/v1/capabilities")
async def list_capabilities():
    """List all registered capabilities"""
    return {"capabilities": registry.list_capabilities()}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "platform": "Project Munde",
        "version": "1.0.0",
        "loaded_domain_packs": ["sahyadri"],
        "registered_agents_count": len(registry.list_agents())
    }
