"""
Project Munde — Query Understanding Agent (Phase 2)
Analyzes user queries to extract structured intent, entities, and required capabilities.
"""
from typing import Dict, Any, List
from munde.agents.base import BaseAgent
import structlog
import json

logger = structlog.get_logger(__name__)

SYSTEM_PROMPT = """
You are the Query Understanding Agent for Project Munde, an agentic AI platform.
Your job is to analyze the user's query and extract structured metadata to help the Orchestrator route and plan the task.

Return ONLY a valid JSON object with the following structure. Do not include markdown formatting or explanations.

{
  "intent": "information_retrieval" | "comparison" | "analysis" | "alert" | "action",
  "entities": {
    "locations": ["string"],
    "resources": ["string"],
    "timeframes": ["string"]
  },
  "capabilities": ["string", "string"],
  "complexity": "simple" | "multi_hop" | "cross_domain",
  "requires_planning": true | false,
  "requires_tools": true | false
}

Available capabilities in the platform include: water, reservoir, irrigation, drought, flood, agriculture, crop, soil, farm, harvest, market_price, health, hospital, medical, phc, chc, bed, disease, land, property, survey, 7/12, satbara, revenue, disaster, emergency, landslide, relief.
"""

class QueryUnderstandingAgent(BaseAgent):
    name = "QueryUnderstanding"
    description = "Analyzes queries to extract structured intent, entities, and capabilities"
    domain = "platform"
    capabilities = ["query_analysis", "intent_detection"]
    
    async def analyze(self, query: str) -> Dict[str, Any]:
        logger.info("query_understanding_analyzing", query=query[:100])
        
        try:
            prompt = f"{SYSTEM_PROMPT}\n\nUSER QUERY: {query}"
            response_text = await self.call_llm(prompt, temperature=0.0)
            
            response_text = response_text.strip().removeprefix("```json").removesuffix("```").strip()
            result = json.loads(response_text)
            
            required_fields = ["intent", "entities", "capabilities", "complexity", "requires_planning", "requires_tools"]
            if all(field in result for field in required_fields):
                logger.info("query_understanding_success", result=result)
                return result
                
        except Exception as e:
            logger.warning("query_understanding_llm_failed", error=str(e))
        
        logger.info("query_understanding_fallback_triggered")
        return self._fallback_analysis(query)
    
    def _fallback_analysis(self, query: str) -> Dict[str, Any]:
        q = query.lower()
        
        if any(w in q for w in ["compare", "vs", "versus", "difference"]):
            intent = "comparison"
            complexity = "multi_hop"
        elif any(w in q for w in ["alert", "warning", "emergency"]):
            intent = "alert"
            complexity = "simple"
        else:
            intent = "information_retrieval"
            complexity = "simple"
            
        caps = []
        if any(w in q for w in ["water", "reservoir", "dam", "jal"]): caps.extend(["water", "reservoir"])
        if any(w in q for w in ["crop", "soil", "farm", "krishi"]): caps.extend(["agriculture", "crop"])
        if any(w in q for w in ["hospital", "health", "bed", "arogya"]): caps.extend(["health", "hospital"])
        if any(w in q for w in ["land", "survey", "7/12", "bhumi"]): caps.extend(["land", "survey"])
        if any(w in q for w in ["flood", "drought", "disaster", "aapda"]): caps.extend(["disaster", "emergency"])
        
        if not caps:
            caps = ["general"]
            
        return {
            "intent": intent,
            "entities": {"locations": [], "resources": [], "timeframes": []},
            "capabilities": list(set(caps)),
            "complexity": complexity,
            "requires_planning": complexity == "multi_hop",
            "requires_tools": False
        }
