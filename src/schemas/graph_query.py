"""
Pydantic models for Knowledge Graph query API.
Strictly typed, validated, and aligned with Data Foundation Section 7.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class GraphEntityResponse(BaseModel):
    """Response model for a single graph entity."""

    id: int
    name: str
    entity_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    location_id: Optional[int] = None


class GraphRelationshipResponse(BaseModel):
    """Response model for a single graph relationship."""

    source: GraphEntityResponse
    relationship_type: str
    target: GraphEntityResponse


class GraphQueryRequest(BaseModel):
    """Request model for graph queries."""

    entity_name: Optional[str] = Field(
        None, description="Name of the entity to query (e.g., 'Pune')"
    )
    entity_type: Optional[str] = Field(
        None, description="Type filter (e.g., 'AdministrativeUnit')"
    )
    relationship_type: Optional[str] = Field(
        None, description="Relationship filter (e.g., 'contains')"
    )
    max_depth: int = Field(default=1, ge=1, le=5, description="Traversal depth (1-5)")
    limit: int = Field(default=50, ge=1, le=500, description="Max results")


class GraphQueryResponse(BaseModel):
    """Response model for graph queries with citations."""

    entities: List[GraphEntityResponse] = Field(default_factory=list)
    relationships: List[GraphRelationshipResponse] = Field(default_factory=list)
    query_summary: str = ""
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.0)
    citations: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
