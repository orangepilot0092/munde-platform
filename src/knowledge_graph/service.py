from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.core.logging_config import get_logger
from src.knowledge_graph.models import (
    AdministrativeUnit,
    GraphEntity,
    GraphRelationship,
)
import json

logger = get_logger(__name__)


class KnowledgeGraphService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_children(self, unit_id: int) -> List[AdministrativeUnit]:
        """Get all direct children of an administrative unit."""
        query = text(
            "SELECT id, name, type, code, parent_id FROM administrative_units WHERE parent_id = :unit_id"
        )
        result = self.db.execute(query, {"unit_id": unit_id})
        return [AdministrativeUnit(**row._mapping) for row in result]

    def find_entity_by_name(self, name: str, entity_type: str) -> Optional[GraphEntity]:
        """Find a specific entity by name and type."""
        query = text(
            "SELECT id, name, entity_type, properties, location_id FROM graph_entities WHERE name = :name AND entity_type = :type LIMIT 1"
        )
        result = self.db.execute(query, {"name": name, "type": entity_type})
        row = result.fetchone()
        if row:
            return GraphEntity(**row._mapping)
        return None

    def add_relationship(self, rel: GraphRelationship):
        """Add a new relationship between two entities."""
        query = text("""
            INSERT INTO graph_relationships (source_id, target_id, relationship_type, properties)
            VALUES (:source_id, :target_id, :relationship_type, :properties)
        """)
        self.db.execute(
            query,
            {
                "source_id": rel.source_id,
                "target_id": rel.target_id,
                "relationship_type": rel.relationship_type,
                "properties": json.dumps(rel.properties) if rel.properties else None,
            },
        )
        self.db.commit()
        logger.info(
            f"Added relationship: {rel.relationship_type} between {rel.source_id} and {rel.target_id}"
        )

    def find_unit_by_coordinate(
        self, lat: float, lon: float
    ) -> Optional[AdministrativeUnit]:
        """Find which administrative unit contains a given coordinate."""
        query = text("""
            SELECT id, name, type, code, parent_id 
            FROM administrative_units 
            WHERE ST_Contains(geometry, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326))
            LIMIT 1
        """)
        result = self.db.execute(query, {"lat": lat, "lon": lon})
        row = result.fetchone()
        if row:
            return AdministrativeUnit(**row._mapping)
        return None
