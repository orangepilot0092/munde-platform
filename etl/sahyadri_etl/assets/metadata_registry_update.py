"""
Dagster Asset: Automated Metadata Registry Update.
Updates the Intelligence Asset registry with fresh quality, lineage, and completeness metrics.
"""

import json
import logging
import os
from datetime import datetime, timezone

import asyncpg
from dagster import AssetExecutionContext, MetadataValue, asset

logger = logging.getLogger(__name__)


@asset(
    name="metadata_registry_weather_nasa_power",
    group_name="governance",
    description="Updates the metadata registry with the latest quality and lineage metrics for NASA POWER weather data.",
    deps=["weather_nasa_power_maharashtra"],
)
async def metadata_registry_weather_nasa_power(context: AssetExecutionContext) -> None:
    """
    Automatically updates the Intelligence Asset registry after successful ingestion.
    """
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    context.log.info("🔄 Updating metadata registry for NASA POWER weather asset...")

    conn = await asyncpg.connect(
        user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
    )

    try:
        # Fetch latest stats from the database
        db_count = await conn.fetchval(
            "SELECT COUNT(*) FROM atlas.maharashtra_weather_daily;"
        )
        latest_date = await conn.fetchval(
            "SELECT MAX(date) FROM atlas.maharashtra_weather_daily;"
        )
        district_count = await conn.fetchval(
            "SELECT COUNT(DISTINCT district_name) FROM atlas.maharashtra_weather_daily;"
        )

        now = datetime.now(timezone.utc)
        dataset_id = "mh-weather-daily-nasa-power-v1"

        # Calculate freshness score (100 if latest date is today/yesterday, decaying by 5 per day older)
        freshness_score = 100.0
        if latest_date:
            days_old = (now.date() - latest_date).days
            freshness_score = max(0.0, 100.0 - (days_old * 5.0))

        update_query = """
            UPDATE sahyadri.metadata_registry
            SET 
                last_updated = $1,
                freshness_score = $2,
                completeness_score = $3,
                metadata = metadata || $4::jsonb
            WHERE dataset_id = $5;
        """

        metadata_update = {
            "last_successful_run": now.isoformat(),
            "total_records": db_count,
            "districts_covered": district_count,
            "latest_data_date": str(latest_date) if latest_date else None,
        }

        await conn.execute(
            update_query,
            now,
            freshness_score,
            100.0,  # Completeness is assumed 100% if pipeline succeeded
            json.dumps(metadata_update),
            dataset_id,
        )

        context.log.info(f"✅ Metadata registry updated for {dataset_id}")
        context.add_output_metadata(
            {
                "dataset_id": MetadataValue.text(dataset_id),
                "records_in_db": MetadataValue.int(db_count),
                "freshness_score": MetadataValue.float(freshness_score),
                "latest_data_date": MetadataValue.text(str(latest_date)),
            }
        )

    except Exception as e:
        context.log.error(f"❌ Failed to update metadata registry: {e}")
        raise
    finally:
        await conn.close()
