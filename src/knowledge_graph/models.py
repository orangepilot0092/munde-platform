from pydantic import BaseModel
from typing import Optional, Dict, Any


class AdministrativeUnit(BaseModel):
    id: int
    name: str
    type: str
    code: Optional[str] = None
    parent_id: Optional[int] = None


class GraphEntity(BaseModel):
    id: int
    name: str
    entity_type: str
    properties: Optional[Dict[str, Any]] = None
    location_id: Optional[int] = None


class GraphRelationship(BaseModel):
    source_id: int
    target_id: int
    relationship_type: str
    properties: Optional[Dict[str, Any]] = None
