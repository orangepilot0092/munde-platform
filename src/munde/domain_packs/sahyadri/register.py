"""
Project Sahyadri Domain Pack — Registration
Registers all Sahyadri agents with the platform.
"""
from munde.runtime.agent_registry import registry
from munde.domain_packs.sahyadri.agents.jalsetu import JalSetuAgent
from munde.domain_packs.sahyadri.agents.krishisetu import KrishiSetuAgent
from munde.domain_packs.sahyadri.agents.arogyasetu import ArogyaSetuAgent
from munde.domain_packs.sahyadri.agents.bhumisetu import BhumiSetuAgent
from munde.domain_packs.sahyadri.agents.aapdasetu import AapdaSetuAgent
import structlog

logger = structlog.get_logger(__name__)

def register_sahyadri_pack():
    """Register all Sahyadri domain pack agents with the platform"""
    logger.info("registering_sahyadri_domain_pack")
    
    agents = [
        JalSetuAgent(),
        KrishiSetuAgent(),
        ArogyaSetuAgent(),
        BhumiSetuAgent(),
        AapdaSetuAgent(),
    ]
    
    for agent in agents:
        registry.register(agent)
    
    logger.info(
        "sahyadri_pack_registered",
        agents_count=len(agents),
        capabilities=registry.list_capabilities()
    )

# Auto-register when imported
register_sahyadri_pack()

# Register platform agents
from munde.agents.platform.query_understanding import QueryUnderstandingAgent
registry.register(QueryUnderstandingAgent())
