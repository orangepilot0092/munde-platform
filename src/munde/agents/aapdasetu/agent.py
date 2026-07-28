"""
AapdaSetu: Disaster Management RAG Agent for Maharashtra.
"""
from typing import Optional, Dict, Any, List
from munde.agents.base import BaseAgent, AgentResponse
import structlog

logger = structlog.get_logger(__name__)

AAPDA_SYSTEM_PROMPT = """
You are AapdaSetu, the official Disaster Management Agent for Project Munde (Maharashtra Government).
Your expertise: Flood/drought alerts, landslide warnings, relief camp locations, and emergency protocols.

STRICT SAFETY RULES:
1. ONLY use the provided "Retrieved Context" to answer the user's query.
2. ALWAYS begin your response with: "⚠️ EMERGENCY NOTICE: If you are in immediate danger, please call 112 (Maharashtra Emergency) or 108 (Ambulance) immediately."
3. If the context does not contain the answer, state: "I do not have real-time disaster data for this specific location. Please contact the district collector's office or call 112."
4. ALWAYS cite the specific district, taluka, alert type, and emergency contact from the context.
"""

class AapdaSetuAgent(BaseAgent):
    name = "AapdaSetu"
    description = "Disaster Management - Flood/drought alerts, relief camps, emergency protocols"
    domain = "disaster"
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("aapdasetu_processing_query", query=query[:100])
        search_results = await self.search_knowledge(query, top_k=3)
        
        if search_results:
            context_text = "\n\n".join([f"Source: {r['name']}\nDetails: {r['description']}" for r in search_results])
            sources = [r['name'] for r in search_results]
        else:
            context_text = "No relevant disaster data found."
            sources = []
            
        rag_prompt = f"{AAPDA_SYSTEM_PROMPT}\n\n--- RETRIEVED CONTEXT ---\n{context_text}\n-------------------------\n\nUSER QUERY: {query}"
        llm_response = await self.call_llm(rag_prompt, temperature=0.0) # Zero temperature for maximum factual strictness in emergencies
        
        avg_similarity = sum(r['similarity_score'] for r in search_results) / len(search_results) if search_results else 0.0
        return self.format_response(answer=llm_response, confidence=round(min(95.0, avg_similarity * 100), 2), sources=sources, metadata={"search_results_count": len(search_results)})
