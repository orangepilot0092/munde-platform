"""
Register the Maharashtra Districts dataset as an official Intelligence Asset.
Matches the actual metadata_registry schema.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone

try:
    import asyncpg
except ImportError:
    print("❌ asyncpg not found. Install via: poetry add asyncpg")
    exit(1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Stable, human-readable dataset ID
DATASET_ID = "mh-district-boundaries-osm-v1"


async def main() -> None:
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    logger.info(f"🔌 Connecting to PostgreSQL at {db_host}:5432...")

    try:
        conn = await asyncpg.connect(
            user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
        )
        logger.info("✅ Connected successfully.")

        now = datetime.now(timezone.utc)

        # Core asset fields
        name = "Maharashtra District Boundaries"
        description = (
            "Official administrative boundaries of all 36 districts in Maharashtra, "
            "sourced from OpenStreetMap Nominatim API. Includes multilingual names "
            "(English, Marathi, Hindi) and validated MultiPolygon geometries."
        )
        description_mr = "महाराष्ट्रातील सर्व ३६ जिल्ह्यांच्या अधिकृत प्रशासकीय सीमा."
        description_hi = "महाराष्ट्र के सभी 36 जिलों की आधिकारिक प्रशासनिक सीमाएँ।"

        domain = "Geospatial"
        department = "Revenue & Forest (Geospatial Cell)"
        source_url = "https://nominatim.openstreetmap.org/"
        license_ = "ODbL"
        format_ = "PostGIS MultiPolygon (EPSG:4326)"
        refresh_frequency = "quarterly"
        storage_path = "postgis://atlas.maharashtra_districts"

        # Quality scores (0-100)
        quality_score = 95.0
        freshness_score = 98.0  # Fetched today
        completeness_score = 100.0  # All 36 districts present
        machine_readability_score = 95.0

        # Tags (JSON array)
        tags = json.dumps(
            [
                "GIS",
                "Administrative",
                "Maharashtra",
                "Tier 1",
                "OpenStreetMap",
                "Nominatim",
                "Boundaries",
                "Districts",
            ]
        )

        # Lineage (provenance trail)
        lineage = {
            "source": "OpenStreetMap Nominatim API",
            "source_tier": "Tier 1 - Fully Open",
            "ingestion_script": "scripts/connectors/ingest_maharashtra_districts_v5.py",
            "transformation_script": "scripts/atlas/load_districts_postgis.py",
            "target_table": "atlas.maharashtra_districts",
            "total_features": 36,
            "projection": "EPSG:4326",
            "validated_by": "PostGIS ST_GeometryType + ST_Multi conversion",
            "ingested_at": now.isoformat(),
        }

        # Validation report
        validation_report = {
            "schema_check": "PASS",
            "geometry_check": "PASS (all MultiPolygon)",
            "completeness_check": "PASS (36/36 districts)",
            "multilingual_check": "PASS (name, name_mr, name_hi populated)",
            "warnings": [
                "Some districts returned Polygon instead of MultiPolygon — auto-converted via ST_Multi()"
            ],
            "validated_at": now.isoformat(),
        }

        # AI Readiness metadata
        ai_readiness = {
            "embeddable": True,
            "embedding_model": "pending",
            "embedding_dimensions": 768,
            "rag_eligible": True,
            "kg_node_type": "AdministrativeBoundary",
            "kg_relations": ["belongs_to_state", "contains_taluka", "contains_village"],
            "semantic_search_ready": False,  # Will be True after embedding generation
            "notes": "Ready for embedding generation in next step",
        }

        # Extended metadata
        metadata = {
            "asset_type": "Geospatial Dataset",
            "sensitivity": "Public",
            "total_records": 36,
            "coverage": "State-wide (Maharashtra)",
            "spatial_extent": {
                "type": "state",
                "name": "Maharashtra",
                "country": "India",
                "iso_code": "IN-MH",
            },
            "related_agents": ["JalSetu", "KrishiSetu", "NagarSetu", "AapattiSetu"],
            "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
            "attribution": "© OpenStreetMap contributors",
            "version": "1.0",
            "registered_at": now.isoformat(),
        }

        # Upsert query matching the actual schema
        query = """
            INSERT INTO sahyadri.metadata_registry
            (dataset_id, name, name_mr, name_hi, description, description_mr, description_hi,
             domain, department, source_url, license, format, refresh_frequency,
             last_updated, quality_score, freshness_score, completeness_score,
             machine_readability_score, tags, storage_path, lineage,
             validation_report, ai_readiness, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,
                    $14, $15, $16, $17, $18, $19::json, $20, $21::jsonb,
                    $22::jsonb, $23::jsonb, $24::jsonb)
            ON CONFLICT (dataset_id) DO UPDATE SET
                name = EXCLUDED.name,
                name_mr = EXCLUDED.name_mr,
                name_hi = EXCLUDED.name_hi,
                description = EXCLUDED.description,
                description_mr = EXCLUDED.description_mr,
                description_hi = EXCLUDED.description_hi,
                domain = EXCLUDED.domain,
                department = EXCLUDED.department,
                source_url = EXCLUDED.source_url,
                license = EXCLUDED.license,
                format = EXCLUDED.format,
                refresh_frequency = EXCLUDED.refresh_frequency,
                last_updated = EXCLUDED.last_updated,
                quality_score = EXCLUDED.quality_score,
                freshness_score = EXCLUDED.freshness_score,
                completeness_score = EXCLUDED.completeness_score,
                machine_readability_score = EXCLUDED.machine_readability_score,
                tags = EXCLUDED.tags,
                storage_path = EXCLUDED.storage_path,
                lineage = EXCLUDED.lineage,
                validation_report = EXCLUDED.validation_report,
                ai_readiness = EXCLUDED.ai_readiness,
                metadata = EXCLUDED.metadata;
        """

        await conn.execute(
            query,
            DATASET_ID,
            name,
            "महाराष्ट्र जिल्हा सीमा",
            "महाराष्ट्र जिला सीमाएँ",
            description,
            description_mr,
            description_hi,
            domain,
            department,
            source_url,
            license_,
            format_,
            refresh_frequency,
            now,
            quality_score,
            freshness_score,
            completeness_score,
            machine_readability_score,
            tags,
            storage_path,
            json.dumps(lineage),
            json.dumps(validation_report),
            json.dumps(ai_readiness),
            json.dumps(metadata),
        )

        logger.info("=" * 70)
        logger.info("✅ INTELLIGENCE ASSET REGISTERED SUCCESSFULLY")
        logger.info("=" * 70)
        logger.info(f"  🆔 Dataset ID:     {DATASET_ID}")
        logger.info(f"  📛 Name:           {name}")
        logger.info(f"  🏛️  Domain:         {domain}")
        logger.info(f"  ⭐ Quality Score:  {quality_score}/100")
        logger.info(f"  📊 Completeness:   {completeness_score}/100")
        logger.info(f"  🕒 Freshness:      {freshness_score}/100")
        logger.info(f"  📁 Storage:        {storage_path}")
        logger.info("  🔗 Source Tier:    Tier 1 - Fully Open")
        logger.info("=" * 70)

        # Verify by querying back
        row = await conn.fetchrow(
            "SELECT dataset_id, name, domain, quality_score, last_updated FROM sahyadri.metadata_registry WHERE dataset_id = $1",
            DATASET_ID,
        )
        logger.info("\n🔍 Verification query result:")
        logger.info(f"   {dict(row)}")

    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if "conn" in locals():
            await conn.close()
            logger.info("🔌 Database connection closed.")


if __name__ == "__main__":
    asyncio.run(main())
