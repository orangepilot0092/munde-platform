"""
Core Maharashtra Ontology for the Unified Knowledge Graph.
Defines the canonical entity types and relationship edges that govern the semantic layer.
Aligned with Data Foundation Section 7: Knowledge Graph Ontology.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class EntityType(str, Enum):
    """Canonical Entity Types for the Maharashtra Digital Twin."""

    ADMINISTRATIVE_UNIT = "AdministrativeUnit"  # State, District, Taluka, Village
    WATER_BODY = "WaterBody"  # River, Reservoir, Lake, Canal
    AGRI_ZONE = "AgriZone"  # Crop region, Soil type zone
    INFRASTRUCTURE = "Infrastructure"  # Dam, Toll Plaza, Hospital, School
    OBSERVATION = "Observation"  # Weather event, AQI reading, Fire alert
    POLICY = "Policy"  # GR, Act, Scheme (e.g., PMFBY)


class EdgeType(str, Enum):
    """Canonical Relationship Edges."""

    # Spatial / Hierarchical
    CONTAINS = "CONTAINS"  # District CONTAINS Taluka
    LOCATED_IN = "LOCATED_IN"  # Reservoir LOCATED_IN District
    FLOWS_THROUGH = "FLOWS_THROUGH"  # River FLOWS_THROUGH District

    # Measurement / Event
    MEASURED_AT = "MEASURED_AT"  # Weather Observation MEASURED_AT District
    IMPACTS = "IMPACTS"  # Fire Alert IMPACTS AgriZone

    # Governance
    GOVERNS = "GOVERNS"  # Policy GOVERNS AgriZone
    SUPPLIES = "SUPPLIES"  # Canal SUPPLIES AgriZone


class GraphNode(BaseModel):
    """Canonical representation of a Knowledge Graph Entity."""

    id: str = Field(..., description="Unique deterministic ID (e.g., 'MH_DIST_PUNE')")
    entity_type: EntityType
    name: str
    name_mr: Optional[str] = Field(
        None, description="Marathi name for multilingual support"
    )
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GraphEdge(BaseModel):
    """Canonical representation of a Knowledge Graph Relationship."""

    source_id: str
    target_id: str
    edge_type: EdgeType
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
