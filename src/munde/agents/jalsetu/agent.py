"""
JalSetu: Water Intelligence RAG Agent for Maharashtra.
"""
from typing import Optional, Dict, Any, List
from munde.agents.base import BaseAgent, AgentResponse
from munde.prompts.library import prompt_library
import structlog

logger = structlog.get_logger(__name__)

JALSETU_SYSTEM_PROMPT = """
You are JalSetu, the official Water Intelligence Agent for Project Munde (Maharashtra Government).
Your expertise: Maharashtra's water resources, reservoirs, irrigation, drought prediction, and flood management.

STRICT RULES:
1. ONLY use the provided "Retrieved Context" to answer the user's query.
2. If the context does not contain the answer, state: "I do not have sufficient real-time data to answer this specific query."
3. ALWAYS cite the specific reservoir name, district, and data source from the context.
4. Provide a confidence score (0-100) based on how directly the context answers the query.
"""

class JalSetuAgent(BaseAgent):
    name = "JalSetu"
    description = "Water Intelligence - Reservoirs, irrigation, drought, floods"
    domain = "water"
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("jalsetu_processing_query", query=query[:100])
        search_results = await self.search_knowledge(query, top_k=3)
        
        if search_results:
            context_text = "\n\n".join([f"Source: {r['name']}\nDetails: {r['description']}\nRelevance Score: {r['similarity_score']}" for r in search_results])
            sources = [r['name'] for r in search_results]
        else:
            context_text = "No relevant data found in the knowledge base."
            sources = []
        
        rag_prompt = f"{JALSETU_SYSTEM_PROMPT}\n\n--- RETRIEVED CONTEXT ---\n{context_text}\n-------------------------\n\nUSER QUERY: {query}\n\nProvide a comprehensive, cited response based ONLY on the context above."
        
        llm_response = await self.call_llm(rag_prompt, temperature=0.1)
        avg_similarity = sum(r['similarity_score'] for r in search_results) / len(search_results) if search_results else 0.0
        confidence = min(95.0, max(40.0, avg_similarity * 100))
        
        return self.format_response(answer=llm_response, confidence=round(confidence, 2), sources=sources, metadata={"search_results_count": len(search_results)})
