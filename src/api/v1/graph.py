from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.knowledge_graph import KnowledgeGraphService
from typing import Optional

router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])


@router.get("/entities")
def list_entities(
    type: Optional[str] = Query(
        None,
        description="Filter by entity type (e.g., River, Crop, Reservoir, District)",
    ),
    db: Session = Depends(get_db),
):
    """List all entities in the Maharashtra Knowledge Graph."""
    service = KnowledgeGraphService(db)
    return service.get_entities(type)


@router.get("/entities/{entity_name}/relationships")
def get_entity_relationships(
    entity_name: str,
    rel: Optional[str] = Query(None, description="Filter by relationship type"),
    db: Session = Depends(get_db),
):
    """Traverse the graph to find all relationships connected to a specific entity."""
    service = KnowledgeGraphService(db)
    rels = service.get_relationships(entity_name, rel)
    return {"entity": entity_name, "relationships": rels}
