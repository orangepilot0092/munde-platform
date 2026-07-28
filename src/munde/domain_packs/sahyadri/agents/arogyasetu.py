"""
Project Sahyadri Domain Pack — ArogyaSetu Agent
Health Intelligence Agent for Maharashtra.
"""
from typing import Optional, Dict, Any, List
from munde.agents.base import BaseAgent, AgentResponse
import structlog

logger = structlog.get_logger(__name__)

AROGYA_SYSTEM_PROMPT = """
You are ArogyaSetu, the official Rural Health Intelligence Agent for Project Sahyadri (Maharashtra Government).
Your expertise: PHC/CHC capacity, bed availability, seasonal disease advisories, public health infrastructure.

STRICT SAFETY RULES:
1. ONLY use the provided "Retrieved Context" to answer the user's query.
2. ALWAYS begin or end your response with: "Disclaimer: I am an AI assistant, not a doctor. For medical emergencies, please call 108 or visit your nearest PHC immediately."
3. If the context does not contain the answer, state: "I do not have real-time data for this specific facility. Please contact the district health office."
4. ALWAYS cite the specific district, taluka, facility name, and data source.
5. Provide a confidence score (0-100) based on how directly the context answers the query.
"""

class ArogyaSetuAgent(BaseAgent):
    name = "ArogyaSetu"
    description = "Health Intelligence - PHC capacity, bed availability, disease advisories"
    domain = "health"
    capabilities = ["health", "hospital", "medical", "phc", "chc", "bed", "disease"]  # NEW
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        logger.info("arogyasetu_processing_query", query=query[:100])
        
        search_results = await self.search_knowledge(query, top_k=3)
        
        if search_results:
            context_text = "\n\n".join([
                f"Source: {r['name']}\nDetails: {r['description']}\nRelevance: {r['similarity_score']}" 
                for r in search_results
            ])
            sources = [r['name'] for r in search_results]
        else:
            context_text = "No relevant health data found in the knowledge base."
            sources = []
        
        rag_prompt = f"""{AROGYA_SYSTEM_PROMPT}

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
