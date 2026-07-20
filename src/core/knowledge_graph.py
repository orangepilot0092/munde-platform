from sqlalchemy.orm import Session
from sqlalchemy import text


class KnowledgeGraphService:
    def __init__(self, db: Session):
        self.db = db

    def get_entities(self, entity_type: str = None):
        if entity_type:
            sql = text(
                "SELECT name, type, metadata FROM graph_entities WHERE type = :type ORDER BY name"
            )
            res = self.db.execute(sql, {"type": entity_type}).fetchall()
        else:
            sql = text(
                "SELECT name, type, metadata FROM graph_entities ORDER BY type, name"
            )
            res = self.db.execute(sql).fetchall()
        return [{"name": r.name, "type": r.type, "metadata": r.metadata} for r in res]

    def get_relationships(self, entity_name: str, relationship_type: str = None):
        # Bidirectional traversal
        sql = text("""
            SELECT 
                e1.name as source, 
                r.relationship_type, 
                e2.name as target,
                e2.type as target_type
            FROM graph_relationships r
            JOIN graph_entities e1 ON r.source_id = e1.id
            JOIN graph_entities e2 ON r.target_id = e2.id
            WHERE (e1.name = :name OR e2.name = :name)
              AND (:rel_type IS NULL OR r.relationship_type = :rel_type)
        """)
        res = self.db.execute(
            sql, {"name": entity_name, "rel_type": relationship_type}
        ).fetchall()
        return [
            {
                "source": r.source,
                "relationship": r.relationship_type,
                "target": r.target,
                "target_type": r.target_type,
            }
            for r in res
        ]
