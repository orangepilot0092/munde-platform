"""
Munde Sahayak: The Chief Orchestrator for Project Munde.
"""
from typing import Optional, Dict, Any
from munde.agents.base import BaseAgent, AgentResponse
from munde.agents.jalsetu.agent import JalSetuAgent
from munde.agents.krishisetu.agent import KrishiSetuAgent
from munde.agents.arogyasetu.agent import ArogyaSetuAgent
from munde.agents.bhumisetu.agent import BhumiSetuAgent
from munde.agents.aapdasetu.agent import AapdaSetuAgent
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
            "bhumisetu": BhumiSetuAgent(),
            "aapdasetu": AapdaSetuAgent(),
        }
    
    def _route_query(self, query: str) -> str:
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in ["hospital", "bed", "fever", "dengue", "malaria", "phc", "doctor", "arogya", "health", "clinic", "patient", "emergency", "108", "vaccine", "aqi", "pollution", "air quality", "pm2.5", "pm10"]):
            return "arogyasetu"
        if any(kw in query_lower for kw in ["flood", "drought", "landslide", "earthquake", "cyclone", "disaster", "aapda", "relief camp", "evacuation", "112"]):
            return "aapdasetu"
        if any(kw in query_lower for kw in ["7/12", "satbara", "survey number", "land use", "soil type", "bhumi", "revenue", "zoning"]):
            return "bhumisetu"
        if any(kw in query_lower for kw in ["water", "reservoir", "dam", "irrigation", "jal", "river", "rainfall", "storage"]):
            return "jalsetu"
        if any(kw in query_lower for kw in ["crop", "farm", "agriculture", "soil", "farmer", "krishi", "harvest", "sugarcane", "cotton", "onion", "moisture", "price", "quintal"]):
            return "krishisetu"
            
        logger.warning("no_agent_match", query=query[:100])
        return "jalsetu"
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("munde_sahayak_routing", query=query[:100])
        target_agent_name = self._route_query(query)
        target_agent = self.agents.get(target_agent_name)
        
        if not target_agent:
            return self.format_response(answer=f"I am currently being trained to handle '{target_agent_name}' queries.", confidence=0.0, sources=[], metadata={"routed_to": "none", "error": "Agent not found"})
        
        logger.info("delegating_to_agent", agent=target_agent_name)
        response = await target_agent.process_query(query, context)
        response.metadata["routed_by"] = "Munde Sahayak"
        response.metadata["target_agent"] = target_agent_name
        response.metadata["original_query"] = query
        return response

    async def get_capabilities(self) -> Dict[str, str]:
        return {name: agent.description for name, agent in self.agents.items()}
