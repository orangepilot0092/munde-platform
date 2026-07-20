"""
Dagster Asset: Knowledge Graph Entity Resolution.
Reads from the Data Atlas and resolves entities into canonical Knowledge Graph nodes.
"""

import logging
import os
import hashlib
from typing import List, Dict, Any

import asyncpg  # type: ignore[import-untyped]
from dagster import AssetExecutionContext, MetadataValue, asset

from src.knowledge_graph.ontology import EntityType, GraphNode

logger = logging.getLogger(__name__)


def generate_deterministic_id(entity_type: str, name: str) -> str:
    """Generates a stable, deterministic ID for an entity."""
    raw = f"{entity_type}:{name}".upper()
    return hashlib.md5(raw.encode()).hexdigest()[:12]


@asset(
    name="kg_resolve_administrative_units",
    group_name="knowledge_graph",
    description="Resolves Maharashtra districts from the Data Atlas into canonical AdministrativeUnit nodes in the Knowledge Graph.",
    deps=["weather_open_meteo_maharashtra"],  # Depends on atlas being populated
)
async def kg_resolve_administrative_units(context: AssetExecutionContext) -> None:
    """
    Pipeline:
    1. Fetch districts from atlas.maharashtra_districts
    2. Map to canonical GraphNode schema
    3. Upsert into knowledge_graph.graph_entities (Idempotent)
    """
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    context.log.info(
        "🧠 Starting Knowledge Graph Entity Resolution for Administrative Units..."
    )

    conn = await asyncpg.connect(
        user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
    )

    try:
        # 1. Fetch source data
        records = await conn.fetch("""
            SELECT name, name_mr, geometry 
            FROM atlas.maharashtra_districts;
        """)

        context.log.info(f"📥 Fetched {len(records)} districts from Data Atlas.")

        # 2. Map to Canonical Nodes
        nodes: List[Dict[str, Any]] = []
        for r in records:
            name = str(r["name"])
            node_id = generate_deterministic_id(
                EntityType.ADMINISTRATIVE_UNIT.value, name
            )

            nodes.append(
                {
                    "id": node_id,
                    "name": name,
                    "name_mr": r["name_mr"],
                    "entity_type": EntityType.ADMINISTRATIVE_UNIT.value,
                    "properties": {"level": "district", "state": "Maharashtra"},
                    "geometry": r["geometry"],  # Pass PostGIS geometry directly
                }
            )

        # 3. Idempotent Upsert into Knowledge Graph
        upsert_query = """
            INSERT INTO knowledge_graph.graph_entities (id, name, name_mr, entity_type, properties, geometry)
            SELECT * FROM unnest(
                $1::text[], $2::text[], $3::text[], $4::text[], $5::jsonb[], $6::geometry[]
            )
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                properties = EXCLUDED.properties,
                geometry = EXCLUDED.geometry;
        """

        # Unnest parameters
        ids = [n["id"] for n in nodes]
        names = [n["name"] for n in nodes]
        names_mr = [n["name_mr"] for n in nodes]
        types = [n["entity_type"] for n in nodes]

        import json

        props = [json.dumps(n["properties"]) for n in nodes]
        geoms = [n["geometry"] for n in nodes]

        await conn.execute(upsert_query, ids, names, names_mr, types, props, geoms)

        context.log.info(
            f"✅ Successfully resolved and upserted {len(nodes)} AdministrativeUnit nodes."
        )

        # 4. Emit Metadata
        total_nodes = await conn.fetchval(
            "SELECT COUNT(*) FROM knowledge_graph.graph_entities;"
        )

        context.add_output_metadata(
            {
                "districts_resolved": MetadataValue.int(len(nodes)),
                "total_graph_nodes": MetadataValue.int(total_nodes),
                "entity_type": MetadataValue.text(EntityType.ADMINISTRATIVE_UNIT.value),
            }
        )

    except Exception as e:
        context.log.error(f"❌ Entity resolution failed: {e}")
        raise
    finally:
        await conn.close()
