"""
Base classes for the Munde Prompt Library.
Defines the structure for all prompts across all agents.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class PromptDifficulty(str, Enum):
    """Difficulty level of the prompt."""
    BASIC = "basic"              # Simple factual queries
    INTERMEDIATE = "intermediate"  # Multi-step reasoning
    ADVANCED = "advanced"        # Cross-domain synthesis
    EXPERT = "expert"            # Policy-level analysis

class PromptCategory(str, Enum):
    """Category of the prompt."""
    SITUATIONAL = "situational"      # Current state analysis
    PREDICTIVE = "predictive"        # Forecasting & risk
    PRESCRIPTIVE = "prescriptive"    # Recommendations
    COMPARATIVE = "comparative"      # Historical comparison
    CROSS_DOMAIN = "cross_domain"    # Multi-agent queries
    CITIZEN_FACING = "citizen_facing"  # Public-facing queries
    OFFICER_FACING = "officer_facing"  # Decision support

class Prompt(BaseModel):
    """A single prompt in the library."""
    id: str = Field(..., description="Unique identifier (e.g., 'jalsetu_001')")
    agent: str = Field(..., description="Target agent (e.g., 'jalsetu')")
    category: PromptCategory
    difficulty: PromptDifficulty
    query: str = Field(..., description="The actual prompt text")
    context: Optional[str] = Field(None, description="Optional context to inject")
    expected_data_sources: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    marathi_translation: Optional[str] = Field(None, description="Marathi version")
    showcase: bool = Field(False, description="If True, featured in hackathon demo")
    notes: Optional[str] = Field(None, description="Internal notes for developers")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True

class PromptLibrary:
    """Central registry of all prompts."""
    
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._by_agent: Dict[str, List[str]] = {}
        self._by_category: Dict[str, List[str]] = {}
        self._by_difficulty: Dict[str, List[str]] = {}
    
    def register(self, prompt: Prompt):
        """Register a new prompt."""
        self._prompts[prompt.id] = prompt
        
        # Index by agent
        if prompt.agent not in self._by_agent:
            self._by_agent[prompt.agent] = []
        self._by_agent[prompt.agent].append(prompt.id)
        
        # Index by category
        if prompt.category not in self._by_category:
            self._by_category[prompt.category] = []
        self._by_category[prompt.category].append(prompt.id)
        
        # Index by difficulty
        if prompt.difficulty not in self._by_difficulty:
            self._by_difficulty[prompt.difficulty] = []
        self._by_difficulty[prompt.difficulty].append(prompt.id)
    
    def get(self, prompt_id: str) -> Optional[Prompt]:
        """Get a prompt by ID."""
        return self._prompts.get(prompt_id)
    
    def get_by_agent(self, agent: str) -> List[Prompt]:
        """Get all prompts for a specific agent."""
        return [self._prompts[pid] for pid in self._by_agent.get(agent, [])]
    
    def get_by_category(self, category: str) -> List[Prompt]:
        """Get all prompts in a category."""
        return [self._prompts[pid] for pid in self._by_category.get(category, [])]
    
    def get_showcase_prompts(self, agent: Optional[str] = None) -> List[Prompt]:
        """Get demo-ready prompts."""
        prompts = self._prompts.values()
        if agent:
            prompts = [p for p in prompts if p.agent == agent]
        return [p for p in prompts if p.showcase]
    
    def stats(self) -> Dict[str, Any]:
        """Library statistics."""
        return {
            "total_prompts": len(self._prompts),
            "by_agent": {agent: len(ids) for agent, ids in self._by_agent.items()},
            "by_category": {cat: len(ids) for cat, ids in self._by_category.items()},
            "by_difficulty": {diff: len(ids) for diff, ids in self._by_difficulty.items()},
            "showcase_count": sum(1 for p in self._prompts.values() if p.showcase)
        }
