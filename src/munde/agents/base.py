"""
Project Munde — Base Agent
Abstract base class for all agents in the platform.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import structlog

logger = structlog.get_logger(__name__)

class AgentResponse(BaseModel):
    """Standard response format for all agents"""
    answer: str
    confidence_score: float
    sources_cited: List[str]
    data_freshness: str
    agent_name: str
    domain: str
    metadata: Dict[str, Any] = {}

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    name: str = "BaseAgent"
    description: str = "Base agent"
    domain: str = "general"
    capabilities: List[str] = []
    
    def __init__(self):
        self.logger = structlog.get_logger(f"agent.{self.name.lower()}")
    
    @abstractmethod
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        pass
    
    async def search_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        DIRECT Python import for vector search. NO HTTP CALLS.
        """
        from munde.knowledge.vector_search import search_similar
        return await search_similar(query, top_k=top_k)
    
    async def call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """Call the LLM with a prompt."""
        from munde.models.llm import call_local_llm
        return await call_local_llm(prompt, temperature=temperature)
    
    def format_response(self, answer: str, confidence: float, sources: List[str], metadata: Dict[str, Any] = None) -> AgentResponse:
        return AgentResponse(
            answer=answer,
            confidence_score=confidence,
            sources_cited=sources,
            data_freshness="2026-07-28",
            agent_name=self.name,
            domain=self.domain,
            metadata=metadata or {}
        )
