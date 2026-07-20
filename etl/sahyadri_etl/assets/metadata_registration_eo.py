"""
Dagster Asset: Automated Metadata Registration for Earth Observation Datasets.
Registers STAC-discovered EO assets into the central metadata registry.
"""

import json
import logging
import os
from datetime import datetime, timezone

import asyncpg  # type: ignore[import-untyped]
from dagster import AssetExecutionContext, MetadataValue, asset

logger = logging.getLogger(__name__)


@asset(
    name="register_eo_stac_metadata",
    group_name="governance",
    description="Registers the Sentinel-2 STAC discovery results into the central metadata registry.",
    deps=["eo_stac_sentinel2_maharashtra"],
)
async def register_eo_stac_metadata(context: AssetExecutionContext) -> None:
    """
    Production Dagster asset for EO metadata registration.
    """
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    context.log.info("🔄 Starting metadata registration for EO STAC dataset...")

    conn = await asyncpg.connect(
        user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
    )

    try:
        dataset_id = "mh-eo-sentinel2-l2a-stac-v1"
        now = datetime.now(timezone.utc).isoformat()

        # Quality score is high because STAC is a standardized, trusted protocol
        quality_score = 90.0

        upsert_query = """
            INSERT INTO sahyadri.metadata_registry 
            (dataset_id, name, name_mr, description, domain, department, source_url, license, tags, quality_score, last_updated, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ON CONFLICT (dataset_id) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                quality_score = EXCLUDED.quality_score,
                last_updated = EXCLUDED.last_updated,
                metadata = sahyadri.metadata_registry.metadata || EXCLUDED.metadata;
        """

        metadata_payload = {
            "ingestion_pipeline": "eo_stac_sentinel2_maharashtra",
            "protocol": "STAC",
            "collection": "sentinel-2-l2a",
            "registered_at": now,
        }

        await conn.execute(
            upsert_query,
            dataset_id,
            "Sentinel-2 L2A Imagery (Maharashtra)",
            "सेंटिनेल-2 एल2ए उपग्रह प्रतिमा (महाराष्ट्र)",
            "Cloud-optimized geotiff metadata for Sentinel-2 Level-2A surface reflectance imagery over Maharashtra, discovered via STAC API.",
            "earth_observation",
            "ISRO / ESA / Microsoft Planetary Computer",
            "https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a",
            "CC-BY-4.0",
            json.dumps(["satellite", "sentinel-2", "ndvi", "maharashtra", "stac"]),
            quality_score,
            now,
            json.dumps(metadata_payload),
        )

        context.log.info(f"✅ Successfully registered/updated EO dataset: {dataset_id}")

        context.add_output_metadata(
            {
                "dataset_id": MetadataValue.text(dataset_id),
                "quality_score": MetadataValue.float(quality_score),
            }
        )

        context.log.info("=" * 70)
        context.log.info("📊 EO METADATA REGISTRATION COMPLETE")
        context.log.info("=" * 70)
        context.log.info(f"  🆔 Dataset ID: {dataset_id}")
        context.log.info(f"  ⭐ Quality Score: {quality_score}/100")
        context.log.info("=" * 70)

    except Exception as e:
        context.log.error(f"❌ EO Metadata registration failed: {e}")
        raise
    finally:
        await conn.close()
        context.log.info("🔌 Database connection closed.")
