"""
Project Sahyadri Domain Pack — JalSetu Agent
"""
from typing import Optional, Dict, Any, List
from munde.agents.base import BaseAgent, AgentResponse
from munde.knowledge.vector_search import search_similar  # <-- EXPLICIT DIRECT IMPORT
import structlog

logger = structlog.get_logger(__name__)

JALSETU_SYSTEM_PROMPT = """
You are JalSetu, the official Water Intelligence Agent.
ONLY use the provided "Retrieved Context". If none, state you don't have the data.
"""

class JalSetuAgent(BaseAgent):
    name = "JalSetu"
    description = "Water Intelligence - Reservoirs, irrigation, drought, floods"
    domain = "water"
    capabilities = ["water", "reservoir", "irrigation", "drought", "flood"]
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("jalsetu_processing_query", query=query[:100])
        
        # DIRECT CALL to vector_search (bypasses any broken base class methods)
        search_results = await search_similar(query, top_k=3)
        logger.info("jalsetu_search_results_count", count=len(search_results))
        
        if search_results:
            context_text = "\n\n".join([
                f"Source: {r['name']}\nDetails: {r['description']}" 
                for r in search_results
            ])
            sources = [r['name'] for r in search_results]
        else:
            context_text = "NO DATA FOUND IN VECTOR DB."
            sources = []
        
        rag_prompt = f"""{JALSETU_SYSTEM_PROMPT}

--- RETRIEVED CONTEXT ---
{context_text}
-------------------------

USER QUERY: {query}"""
        
        # Fallback LLM call if the model module isn't ready, otherwise use base class
        try:
            llm_response = await self.call_llm(rag_prompt, temperature=0.0)
        except Exception as e:
            logger.error("llm_call_failed", error=str(e))
            llm_response = f"LLM call failed: {e}. Context was: {context_text[:200]}"
        
        avg_similarity = sum(r.get('similarity_score', 0.5) for r in search_results) / len(search_results) if search_results else 0.0
        confidence = min(95.0, max(40.0, avg_similarity * 100))
        
        return self.format_response(
            answer=llm_response,
            confidence=round(confidence, 2),
            sources=sources,
            metadata={
                "search_results_count": len(search_results),
                "debug_top_result": search_results[0]['name'] if search_results else None
            }
        )
