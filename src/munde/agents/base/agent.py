"""
Base agent class for all specialized agents in Project Munde.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import httpx
import structlog

logger = structlog.get_logger(__name__)

class AgentResponse(BaseModel):
    """Standard response format for all agents."""
    answer: str
    confidence_score: float = Field(ge=0, le=100)
    sources_cited: List[str] = []
    data_freshness: Optional[str] = None
    agent_name: str
    domain: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BaseAgent(ABC):
    name: str = "BaseAgent"
    description: str = "Base agent"
    domain: str = "general"
    
    def __init__(self):
        self.llm_endpoint = "http://192.168.29.96:11434/api/generate"
        self.llm_model = "qwen2.5:14b"
        self.search_endpoint = "http://192.168.29.20:8004/api/v1/search/semantic"
        self.logger = structlog.get_logger(f"munde.agents.{self.name.lower().replace(' ', '_')}")
    
    async def search_knowledge(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(self.search_endpoint, json={"query": query, "top_k": top_k})
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error("search_failed", error=str(e))
            return []

    async def call_llm(self, prompt: str, temperature: float = 0.1) -> str:
        payload = {"model": self.llm_model, "prompt": prompt, "stream": False, "options": {"temperature": temperature, "top_p": 0.9}}
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.llm_endpoint, json=payload)
                response.raise_for_status()
                return response.json().get("response", "").strip()
        except Exception as e:
            self.logger.error("llm_call_failed", error=str(e))
            return "Error: Unable to generate response from AI node."

    def format_response(self, answer: str, confidence: float, sources: List[str], metadata: Optional[Dict] = None) -> AgentResponse:
        return AgentResponse(
            answer=answer, confidence_score=confidence, sources_cited=sources,
            agent_name=self.name, domain=self.domain, metadata=metadata or {},
            data_freshness=datetime.utcnow().strftime("%Y-%m-%d")
        )
