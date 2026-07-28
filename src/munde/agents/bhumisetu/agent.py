"""
BhumiSetu: Land Intelligence RAG Agent for Maharashtra.
"""
from typing import Optional, Dict, Any, List
from munde.agents.base import BaseAgent, AgentResponse
import structlog

logger = structlog.get_logger(__name__)

BHUMI_SYSTEM_PROMPT = """
You are BhumiSetu, the official Land Intelligence Agent for Project Munde (Maharashtra Government).
Your expertise: 7/12 extracts (Satbara), land use zoning, soil suitability, and revenue records.

STRICT RULES:
1. ONLY use the provided "Retrieved Context" to answer the user's query.
2. If the context does not contain the answer, state: "I do not have real-time land record data for this specific survey number or village. Please check the official Mahabhulekh portal."
3. ALWAYS cite the specific district, taluka, village, and survey number from the context.
4. Provide a confidence score (0-100) based on data completeness.
"""

class BhumiSetuAgent(BaseAgent):
    name = "BhumiSetu"
    description = "Land Intelligence - 7/12 extracts, land use, soil suitability"
    domain = "land"
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("bhumisetu_processing_query", query=query[:100])
        search_results = await self.search_knowledge(query, top_k=3)
        
        if search_results:
            context_text = "\n\n".join([f"Source: {r['name']}\nDetails: {r['description']}" for r in search_results])
            sources = [r['name'] for r in search_results]
        else:
            context_text = "No relevant land data found."
            sources = []
            
        rag_prompt = f"{BHUMI_SYSTEM_PROMPT}\n\n--- RETRIEVED CONTEXT ---\n{context_text}\n-------------------------\n\nUSER QUERY: {query}"
        llm_response = await self.call_llm(rag_prompt, temperature=0.0)
        
        avg_similarity = sum(r['similarity_score'] for r in search_results) / len(search_results) if search_results else 0.0
        return self.format_response(answer=llm_response, confidence=round(min(95.0, avg_similarity * 100), 2), sources=sources, metadata={"search_results_count": len(search_results)})
