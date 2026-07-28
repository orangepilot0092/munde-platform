"""
Project Munde — Agent Registry
Generic registry for managing agents from all domain packs.
"""
from typing import Dict, List, Optional
from munde.agents.base import BaseAgent
import structlog

logger = structlog.get_logger(__name__)

class AgentRegistry:
    """
    Central registry for all agents in the platform.
    Domain packs register their agents here.
    """
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._capabilities: Dict[str, List[str]] = {}  # capability -> [agent_names]
    
    def register(self, agent: BaseAgent) -> None:
        """Register an agent with the platform"""
        if agent.name in self._agents:
            logger.warning("agent_already_registered", agent_name=agent.name)
            return
        
        self._agents[agent.name] = agent
        
        # Index by capabilities
        for capability in agent.capabilities:
            if capability not in self._capabilities:
                self._capabilities[capability] = []
            self._capabilities[capability].append(agent.name)
        
        logger.info("agent_registered", agent_name=agent.name, capabilities=agent.capabilities)
    
    def get(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name"""
        return self._agents.get(name)
    
    def find_by_capability(self, capability: str) -> List[BaseAgent]:
        """Find all agents that have a specific capability"""
        agent_names = self._capabilities.get(capability, [])
        return [self._agents[name] for name in agent_names if name in self._agents]
    
    def list_agents(self) -> List[str]:
        """List all registered agent names"""
        return list(self._agents.keys())
    
    def list_capabilities(self) -> List[str]:
        """List all registered capabilities"""
        return list(self._capabilities.keys())
    
    def get_agent_info(self, name: str) -> Optional[Dict]:
        """Get detailed info about an agent"""
        agent = self.get(name)
        if not agent:
            return None
        
        return {
            "name": agent.name,
            "description": agent.description,
            "domain": agent.domain,
            "capabilities": agent.capabilities,
        }

# Global registry instance
registry = AgentRegistry()
