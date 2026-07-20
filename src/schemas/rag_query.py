"""
Pydantic models for Production RAG Query API.
Enforces AI Engineering Principles: Citations mandatory, Confidence mandatory.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A single citation pointing to a trusted source."""

    source_id: str = Field(..., description="Unique identifier of the source asset")
    source_name: str = Field(..., description="Human-readable name of the source")
    source_type: str = Field(
        ...,
        description="Type of source (e.g., 'dataset', 'document', 'knowledge_graph')",
    )
    relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Relevance score of this citation"
    )


class RAGQueryRequest(BaseModel):
    """Request model for RAG queries."""

    query: str = Field(
        ..., min_length=3, max_length=2000, description="The natural language query"
    )
    domain: Optional[str] = Field(
        None, description="Optional domain filter (e.g., 'agriculture', 'water')"
    )
    include_knowledge_graph: bool = Field(
        default=True,
        description="Whether to enrich context with Knowledge Graph relationships",
    )
    max_results: int = Field(
        default=5, ge=1, le=20, description="Maximum number of sources to retrieve"
    )


class RAGQueryResponse(BaseModel):
    """Response model for RAG queries."""

    answer: str = Field(..., description="The generated, evidence-based answer")
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Overall confidence in the answer (0.0 to 1.0)"
    )
    citations: List[Citation] = Field(
        ..., description="Mandatory list of citations supporting the answer"
    )
    reasoning_steps: List[str] = Field(
        default_factory=list, description="High-level steps taken to derive the answer"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution metadata (latency, model used, etc.)",
    )
