"""
Project Sahyadri Domain Pack — KrishiSetu Agent
Agriculture Intelligence Agent for Maharashtra.
"""
from typing import Optional, Dict, Any, List
from munde.agents.base import BaseAgent, AgentResponse
import structlog

logger = structlog.get_logger(__name__)

KRISHISETU_SYSTEM_PROMPT = """
You are KrishiSetu, the official Agriculture Intelligence Agent for Project Sahyadri (Maharashtra Government).
Your expertise: Crop advisories, soil health, market prices, farming recommendations.

STRICT RULES:
1. ONLY use the provided "Retrieved Context" to answer the user's query.
2. If the context does not contain the answer, state: "I do not have sufficient real-time agricultural data to answer this specific query. Please consult your local Krishi Seva Kendra."
3. ALWAYS cite the specific district, taluka, crop, and data source from the context.
4. Provide a confidence score (0-100) based on data completeness.
"""

class KrishiSetuAgent(BaseAgent):
    name = "KrishiSetu"
    description = "Agriculture Intelligence - Crop advisories, soil health, market prices"
    domain = "agriculture"
    capabilities = ["agriculture", "crop", "soil", "farm", "harvest", "market_price"]  # NEW
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("krishisetu_processing_query", query=query[:100])
        
        search_results = await self.search_knowledge(query, top_k=3)
        
        if search_results:
            context_text = "\n\n".join([
                f"Source: {r['name']}\nDetails: {r['description']}\nRelevance: {r['similarity_score']}" 
                for r in search_results
            ])
            sources = [r['name'] for r in search_results]
        else:
            context_text = "No relevant agricultural data found in the knowledge base."
            sources = []
        
        rag_prompt = f"""{KRISHISETU_SYSTEM_PROMPT}

--- RETRIEVED CONTEXT ---
{context_text}
-------------------------

USER QUERY: {query}

Provide a comprehensive, cited response based ONLY on the context above."""
        
        llm_response = await self.call_llm(rag_prompt, temperature=0.0)
        
        avg_similarity = sum(r['similarity_score'] for r in search_results) / len(search_results) if search_results else 0.0
        confidence = min(95.0, max(40.0, avg_similarity * 100))
        
        return self.format_response(
            answer=llm_response,
            confidence=round(confidence, 2),
            sources=sources,
            metadata={"search_results_count": len(search_results)}
        )
