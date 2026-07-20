from sqlalchemy import text
from sqlalchemy.orm import Session
from src.core.embeddings import EmbeddingService
from src.core.logging import get_logger

logger = get_logger(__name__)


class RAGContextAssembler:
    def __init__(self, db: Session):
        self.db = db
        self.es = EmbeddingService()

    def get_policy_context(self, query: str, limit: int = 2) -> list:
        """Retrieve relevant policy documents from pgvector."""
        vec = self.es.generate_embedding(query)
        vec_str = "[" + ",".join(str(x) for x in vec) + "]"

        sql = text("""
            SELECT content, 1 - (embedding <=> CAST(:vec AS vector)) as score
            FROM document_chunks
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:vec AS vector)
            LIMIT :limit
        """)
        res = self.db.execute(sql, {"vec": vec_str, "limit": limit}).fetchall()
        return [{"text": r.content, "score": float(r.score)} for r in res]

    def get_geospatial_context(self, district: str) -> dict:
        """Retrieve geospatial metrics for a specific district."""
        sql = text("""
            SELECT name, area_sq_km, ST_Y(centroid) as lat, ST_X(centroid) as lon
            FROM administrative_units
            WHERE name = :name AND type = 'District'
        """)
        res = self.db.execute(sql, {"name": district}).first()
        if res:
            return {
                "district": res.name,
                "area_sq_km": round(res.area_sq_km, 2),
                "lat": res.lat,
                "lon": res.lon,
            }
        return {}

    def get_knowledge_graph_context(self, entity: str) -> list:
        """Retrieve relationships for an entity from the Knowledge Graph."""
        sql = text("""
            SELECT e1.name as source, r.relationship_type, e2.name as target, e2.type as target_type
            FROM graph_relationships r
            JOIN graph_entities e1 ON r.source_id = e1.id
            JOIN graph_entities e2 ON r.target_id = e2.id
            WHERE e1.name = :entity OR e2.name = :entity
            LIMIT 10
        """)
        res = self.db.execute(sql, {"entity": entity}).fetchall()
        return [
            {
                "source": r.source,
                "relation": r.relationship_type,
                "target": r.target,
                "type": r.target_type,
            }
            for r in res
        ]

    def assemble_context(
        self, query: str, district: str = "Pune", entity: str = "Sugarcane"
    ) -> dict:
        """Assemble multi-domain context for RAG."""
        logger.info(f"Assembling RAG context for query: {query}")

        policies = self.get_policy_context(query)
        geo = self.get_geospatial_context(district)
        kg = self.get_knowledge_graph_context(entity)

        # Construct the system prompt for the LLM
        system_prompt = f"""You are an AI advisor for Project Sahyadri, an intelligence platform for Maharashtra.
Use the following verified context to answer the user's query accurately and professionally.

[GEOGRAPHIC CONTEXT - {district}]
Area: {geo.get("area_sq_km", "Unknown")} sq km
Coordinates: {geo.get("lat", "Unknown")}, {geo.get("lon", "Unknown")}

[KNOWLEDGE GRAPH CONTEXT - {entity}]
Relationships: {kg}

[POLICY & DOCUMENT CONTEXT]
{[p["text"] for p in policies]}
"""
        return {
            "query": query,
            "system_prompt": system_prompt,
            "retrieved_policies": len(policies),
            "geospatial_data": geo,
            "knowledge_graph_facts": len(kg),
        }
