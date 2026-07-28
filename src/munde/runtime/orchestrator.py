"""
Project Munde — Master Orchestrator
Routes queries to appropriate agents based on structured intent from Query Understanding.
"""
from typing import Dict, Any, Optional, List
from munde.runtime.agent_registry import registry
from munde.agents.base import AgentResponse
from munde.agents.platform.query_understanding import QueryUnderstandingAgent
import structlog

logger = structlog.get_logger(__name__)

class Orchestrator:
    """
    Generic orchestrator that routes queries based on structured intent.
    """
    
    def __init__(self):
        self.registry = registry
        # Instantiate the Query Understanding Agent
        self.query_understanding = QueryUnderstandingAgent()
    
    async def process_query(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process a query by:
        1. Analyzing intent via Query Understanding Agent
        2. Finding suitable agents based on extracted capabilities
        3. Executing the best agent
        4. Returning the response
        """
        logger.info("orchestrator_processing", query=query[:100])
        
        # Step 1: Structured Intent Analysis
        intent_data = await self.query_understanding.analyze(query)
        logger.info("intent_analyzed", intent=intent_data.get("intent"), complexity=intent_data.get("complexity"))
        
        # Step 2: Find agents that match the required capabilities
        required_caps = intent_data.get("capabilities", [])
        suitable_agents = []
        
        for cap in required_caps:
            agents_for_cap = self.registry.find_by_capability(cap)
            for agent in agents_for_cap:
                if agent not in suitable_agents:
                    suitable_agents.append(agent)
        
        if not suitable_agents:
            logger.warning("no_suitable_agents", capabilities=required_caps)
            return self._fallback_response(query)
        
        # Step 3: Execute the first suitable agent
        # TODO (Phase 3): Pass this to the Planner Agent if requires_planning is True
        agent = suitable_agents[0]
        logger.info("routing_to_agent", agent_name=agent.name, capabilities_matched=required_caps)
        
        response = await agent.process_query(query, context)
        
        # Step 4: Enrich response with orchestration metadata
        response.metadata["orchestrator"] = "MundeOrchestrator"
        response.metadata["routed_to"] = agent.name
        response.metadata["intent_analysis"] = intent_data
        
        return response
    
    def _fallback_response(self, query: str) -> AgentResponse:
        """Fallback response when no suitable agent is found"""
        return AgentResponse(
            answer="I do not have a specialized agent for this query. Please try rephrasing or asking about water, agriculture, health, land, or disaster management.",
            confidence_score=0.0,
            sources_cited=[],
            data_freshness="N/A",
            agent_name="Orchestrator",
            domain="general",
            metadata={"error": "no_suitable_agent"}
        )

# Global orchestrator instance
orchestrator = Orchestrator()
