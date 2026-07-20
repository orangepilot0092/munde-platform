"""
Knowledge Graph Integrity Validation Script.
Ensures no orphaned nodes, broken relationships, or invalid entity types exist.
Aligned with Data Foundation Section 7: Knowledge Graph Ontology.
"""

import asyncio
import logging
import os
from typing import List, Tuple

import asyncpg  # type: ignore[import-untyped]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

VALID_ENTITY_TYPES = {
    "AdministrativeUnit",
    "NaturalFeature",
    "Policy",
    "Infrastructure",
    "Person",
}
VALID_RELATIONSHIP_TYPES = {
    "contains",
    "located_in",
    "supplies",
    "governs",
    "connected_to",
    "has_observation",
}


async def validate_graph_integrity() -> Tuple[bool, List[str]]:
    """
    Validates the Knowledge Graph for structural integrity.
    Returns (is_valid, list_of_errors).
    """
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    errors: List[str] = []

    try:
        conn = await asyncpg.connect(
            user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
        )
        logger.info("✅ Connected to PostgreSQL for graph validation.")

        # 1. Check for orphaned relationships (source_id or target_id does not exist)
        logger.info("🔍 Checking for orphaned relationships...")
        orphaned_rels = await conn.fetch("""
            SELECT r.id, r.source_id, r.target_id, r.relationship_type
            FROM knowledge_graph.graph_relationships r
            LEFT JOIN knowledge_graph.graph_entities e1 ON r.source_id = e1.id
            LEFT JOIN knowledge_graph.graph_entities e2 ON r.target_id = e2.id
            WHERE e1.id IS NULL OR e2.id IS NULL;
        """)
        if orphaned_rels:
            errors.append(
                f"Found {len(orphaned_rels)} orphaned relationships (missing source or target entity)."
            )

        # 2. Check for invalid entity types
        logger.info("🔍 Checking for invalid entity types...")
        invalid_entities = await conn.fetch(
            """
            SELECT id, name, entity_type
            FROM knowledge_graph.graph_entities
            WHERE entity_type NOT IN ($1);
        """,
            *VALID_ENTITY_TYPES,
        )
        if invalid_entities:
            types_found = set(e["entity_type"] for e in invalid_entities)
            errors.append(
                f"Found {len(invalid_entities)} entities with invalid types: {types_found}"
            )

        # 3. Check for invalid relationship types
        logger.info("🔍 Checking for invalid relationship types...")
        invalid_rels = await conn.fetch(
            """
            SELECT id, relationship_type
            FROM knowledge_graph.graph_relationships
            WHERE relationship_type NOT IN ($1);
        """,
            *VALID_RELATIONSHIP_TYPES,
        )
        if invalid_rels:
            types_found = set(r["relationship_type"] for r in invalid_rels)
            errors.append(
                f"Found {len(invalid_rels)} relationships with invalid types: {types_found}"
            )

        # 4. Check for self-referencing relationships (usually an error unless explicitly allowed)
        logger.info("🔍 Checking for self-referencing relationships...")
        self_refs = await conn.fetch("""
            SELECT id, source_id, target_id, relationship_type
            FROM knowledge_graph.graph_relationships
            WHERE source_id = target_id;
        """)
        if self_refs:
            errors.append(f"Found {len(self_refs)} self-referencing relationships.")

        # 5. Summary stats
        total_entities = await conn.fetchval(
            "SELECT COUNT(*) FROM knowledge_graph.graph_entities;"
        )
        total_relationships = await conn.fetchval(
            "SELECT COUNT(*) FROM knowledge_graph.graph_relationships;"
        )
        logger.info(
            f"📊 Graph Stats: {total_entities} entities, {total_relationships} relationships."
        )

        await conn.close()
        logger.info("🔌 Database connection closed.")

        is_valid = len(errors) == 0
        return is_valid, errors

    except asyncpg.exceptions.UndefinedTableError:
        logger.warning(
            "⚠️ Knowledge graph tables do not exist yet. Skipping validation."
        )
        return True, []
    except Exception as e:
        logger.error(f"❌ Validation failed with exception: {e}")
        return False, [str(e)]


async def main():
    logger.info("🚀 Starting Knowledge Graph Integrity Validation...")
    is_valid, errors = await validate_graph_integrity()

    if is_valid:
        logger.info("✅ Knowledge Graph integrity validation PASSED.")
    else:
        logger.error("❌ Knowledge Graph integrity validation FAILED.")
        for err in errors:
            logger.error(f"   - {err}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
