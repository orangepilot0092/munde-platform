"""
API routes for Project Munde agents.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
from munde.agents.jalsetu.agent import JalSetuAgent
from munde.agents.munde_sahayak.agent import MundeSahayakAgent
from munde.agents.base import AgentResponse

router = APIRouter(prefix="/agents", tags=["Project Munde Agents"])

class AgentQueryRequest(BaseModel):
    query: str = Field(..., description="User query for the agent")
    context: Optional[Dict] = Field(None, description="Optional additional context")

class AgentQueryResponse(BaseModel):
    response: AgentResponse

class OrchestratorQueryResponse(BaseModel):
    response: AgentResponse
    available_agents: Dict[str, str]

@router.post("/jalsetu/ask", response_model=AgentQueryResponse)
async def ask_jalsetu(request: AgentQueryRequest):
    """Ask JalSetu a water-related question."""
    try:
        agent = JalSetuAgent()
        result = await agent.process_query(request.query, request.context)
        return AgentQueryResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@router.post("/munde-sahayak/ask", response_model=OrchestratorQueryResponse)
async def ask_munde_sahayak(request: AgentQueryRequest):
    """Ask Munde Sahayak (Chief Orchestrator) a question."""
    try:
        orchestrator = MundeSahayakAgent()
        result = await orchestrator.process_query(request.query, request.context)
        capabilities = await orchestrator.get_capabilities()
        
        return OrchestratorQueryResponse(
            response=result,
            available_agents=capabilities
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator failed: {str(e)}")
