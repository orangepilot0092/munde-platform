"""
Munde Sahayak: The Chief Orchestrator for Project Munde.
Routes queries to the appropriate specialized domain agent.
"""
from typing import Optional, Dict, Any, List
from munde.agents.base import BaseAgent, AgentResponse
from munde.agents.jalsetu.agent import JalSetuAgent
from munde.agents.krishisetu.agent import KrishiSetuAgent
from munde.agents.arogyasetu.agent import ArogyaSetuAgent
import structlog

logger = structlog.get_logger(__name__)

class MundeSahayakAgent(BaseAgent):
    name = "Munde Sahayak"
    description = "Chief Orchestrator - Routes queries to the correct domain expert"
    domain = "orchestration"
    
    def __init__(self):
        super().__init__()
        self.agents = {
            "jalsetu": JalSetuAgent(),
            "krishisetu": KrishiSetuAgent(),
            "arogyasetu": ArogyaSetuAgent(),
        }
    
    def _route_query(self, query: str) -> str:
        query_lower = query.lower()
        
        # 1. Health keywords (Check FIRST to avoid collision with generic words like "advisory")
        health_keywords = ["hospital", "bed", "fever", "dengue", "malaria", "phc", "doctor", "arogya", "health", "clinic", "patient", "emergency", "108", "vaccine"]
        if any(kw in query_lower for kw in health_keywords):
            return "arogyasetu"
        
        # 2. Water domain keywords
        water_keywords = ["water", "reservoir", "dam", "irrigation", "drought", "flood", "jal", "river", "rainfall", "storage", "mula", "khadakwasla", "mulshi", "gangapur", "jayakwadi", "pench"]
        if any(kw in query_lower for kw in water_keywords):
            return "jalsetu"
        
        # 3. Agriculture domain keywords (Removed "advisory" as it is too generic)
        agri_keywords = ["crop", "farm", "agriculture", "soil", "farmer", "krishi", "harvest", "sugarcane", "cotton", "onion", "grapes", "rice", "soybean", "moisture", "price", "quintal"]
        if any(kw in query_lower for kw in agri_keywords):
            return "krishisetu"
        
        logger.warning("no_agent_match", query=query[:100])
        return "jalsetu" # Default fallback
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("munde_sahayak_routing", query=query[:100])
        
        target_agent_name = self._route_query(query)
        target_agent = self.agents.get(target_agent_name)
        
        if not target_agent:
            return self.format_response(
                answer=f"I am currently being trained to handle '{target_agent_name}' queries.",
                confidence=0.0, sources=[], metadata={"routed_to": "none", "error": "Agent not found"}
            )
        
        logger.info("delegating_to_agent", agent=target_agent_name)
        response = await target_agent.process_query(query, context)
        
        response.metadata["routed_by"] = "Munde Sahayak"
        response.metadata["target_agent"] = target_agent_name
        response.metadata["original_query"] = query
        
        return response

    async def get_capabilities(self) -> Dict[str, str]:
        return {name: agent.description for name, agent in self.agents.items()}
