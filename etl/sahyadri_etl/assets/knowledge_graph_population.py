"""
Dagster Asset: Knowledge Graph Population for Maharashtra.
Maps ingested Intelligence Assets (Districts, Rivers, Weather) into
graph_entities and graph_relationships for multi-hop reasoning.
"""

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import asyncpg  # type: ignore[import-untyped]
from dagster import AssetExecutionContext, MetadataValue, asset

logger = logging.getLogger(__name__)


async def _upsert_entity(
    conn: asyncpg.Connection,
    name: str,
    entity_type: str,
    properties: Dict[str, Any],
    location_id: Optional[int] = None,
) -> int:
    """Upsert a graph entity and return its ID."""
    query = """
        INSERT INTO knowledge_graph.graph_entities 
        (name, entity_type, properties, location_id, created_at, updated_at)
        VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT (name, entity_type) DO UPDATE SET
            properties = EXCLUDED.properties,
            location_id = COALESCE(EXCLUDED.location_id, graph_entities.location_id),
            updated_at = CURRENT_TIMESTAMP
        RETURNING id;
    """
    row = await conn.fetchrow(query, name, entity_type, properties, location_id)
    return int(row["id"]) if row else 0


async def _upsert_relationship(
    conn: asyncpg.Connection,
    source_id: int,
    target_id: int,
    relationship_type: str,
) -> None:
    """Upsert a graph relationship."""
    query = """
        INSERT INTO knowledge_graph.graph_relationships 
        (source_id, target_id, relationship_type, created_at)
        VALUES ($1, $2, $3, CURRENT_TIMESTAMP)
        ON CONFLICT (source_id, target_id, relationship_type) DO NOTHING;
    """
    await conn.execute(query, source_id, target_id, relationship_type)


@asset(
    name="knowledge_graph_maharashtra_base",
    group_name="knowledge_graph",
    description="Populates the Knowledge Graph with base Maharashtra entities (Districts, Rivers) and their relationships.",
    deps=["weather_nasa_power_maharashtra"],  # Ensures data is fresh before graphing
)
async def knowledge_graph_maharashtra_base(context: AssetExecutionContext) -> None:
    """
    Production Dagster asset for Knowledge Graph population.

    Pipeline:
    1. Fetch districts and create 'AdministrativeUnit' entities.
    2. Fetch rivers and create 'NaturalFeature' entities.
    3. Establish 'contains' relationships (District -> River).
    4. Emit graph integrity metrics.
    """
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    context.log.info("🚀 Starting Knowledge Graph population pipeline...")

    conn = await asyncpg.connect(
        user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
    )

    try:
        # Ensure schema exists
        await conn.execute("CREATE SCHEMA IF NOT EXISTS knowledge_graph;")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_graph.graph_entities (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                entity_type VARCHAR(100) NOT NULL,
                properties JSONB DEFAULT '{}',
                location_id INTEGER,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (name, entity_type)
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_graph.graph_relationships (
                id SERIAL PRIMARY KEY,
                source_id INTEGER REFERENCES knowledge_graph.graph_entities(id) ON DELETE CASCADE,
                target_id INTEGER REFERENCES knowledge_graph.graph_entities(id) ON DELETE CASCADE,
                relationship_type VARCHAR(100) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (source_id, target_id, relationship_type)
            );
        """)
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_graph_entities_type ON knowledge_graph.graph_entities(entity_type);"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_graph_rel_source ON knowledge_graph.graph_relationships(source_id);"
        )

        context.log.info("📊 Schema verified. Fetching source data...")

        # 1. Process Districts
        districts = await conn.fetch("""
            SELECT name, ST_AsGeoJSON(geometry) as geom_json 
            FROM atlas.maharashtra_districts 
            ORDER BY name;
        """)

        district_ids: Dict[str, int] = {}
        for row in districts:
            entity_id = await _upsert_entity(
                conn=conn,
                name=str(row["name"]),
                entity_type="AdministrativeUnit",
                properties={"geometry": row["geom_json"], "level": "district"},
            )
            district_ids[str(row["name"])] = entity_id

        context.log.info(
            f"✅ Processed {len(district_ids)} AdministrativeUnit entities."
        )

        # 2. Process Rivers and link to Districts
        # We use a spatial join to find which district contains each river centroid
        rivers = await conn.fetch("""
            SELECT r.name, r.waterway_type, d.name as district_name
            FROM atlas.maharashtra_rivers r
            LEFT JOIN atlas.maharashtra_districts d 
              ON ST_Contains(d.geometry, r.geometry)
            WHERE r.name != 'Unknown'
            ORDER BY r.name;
        """)

        river_count = 0
        relationship_count = 0

        for row in rivers:
            river_name = str(row["name"])
            district_name = (
                str(row["district_name"]) if row["district_name"] else "Maharashtra"
            )
            waterway_type = str(row["waterway_type"])

            river_id = await _upsert_entity(
                conn=conn,
                name=river_name,
                entity_type="NaturalFeature",
                properties={"feature_type": waterway_type, "state": "Maharashtra"},
            )
            river_count += 1

            # Link river to district
            if district_name in district_ids:
                await _upsert_relationship(
                    conn=conn,
                    source_id=district_ids[district_name],
                    target_id=river_id,
                    relationship_type="contains",
                )
                relationship_count += 1

        context.log.info(f"✅ Processed {river_count} NaturalFeature entities.")
        context.log.info(f"✅ Created {relationship_count} 'contains' relationships.")

        # 3. Emit Metrics
        total_entities = await conn.fetchval(
            "SELECT COUNT(*) FROM knowledge_graph.graph_entities;"
        )
        total_relationships = await conn.fetchval(
            "SELECT COUNT(*) FROM knowledge_graph.graph_relationships;"
        )

        context.add_output_metadata(
            {
                "total_entities": MetadataValue.int(total_entities),
                "total_relationships": MetadataValue.int(total_relationships),
                "districts_processed": MetadataValue.int(len(district_ids)),
                "rivers_processed": MetadataValue.int(river_count),
                "relationships_created": MetadataValue.int(relationship_count),
                "timestamp": MetadataValue.text(datetime.now(timezone.utc).isoformat()),
            }
        )

        context.log.info("=" * 70)
        context.log.info("📊 KNOWLEDGE GRAPH POPULATION COMPLETE")
        context.log.info("=" * 70)
        context.log.info(f"  🧠 Total Entities: {total_entities}")
        context.log.info(f"  🔗 Total Relationships: {total_relationships}")
        context.log.info("=" * 70)

    except Exception as e:
        context.log.error(f"❌ Knowledge Graph population failed: {e}")
        raise
    finally:
        await conn.close()
        context.log.info("🔌 Database connection closed.")
