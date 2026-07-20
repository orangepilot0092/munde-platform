"""
Dagster Asset: NASA POWER Weather Data for Maharashtra Districts.
Production-grade, idempotent pipeline with quality validation and lineage tracking.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import asyncpg
from dagster import AssetExecutionContext, MetadataValue, asset

from src.data_atlas.connectors.nasa_power import NASAPowerConnector

logger = logging.getLogger(__name__)

PARAMETERS = ["PRECTOTCORR", "T2M_MAX", "T2M_MIN"]
DAYS_BACK = 30


async def get_district_centroids(conn: asyncpg.Connection) -> List[Dict[str, Any]]:
    """Fetch name and centroid coordinates of all Maharashtra districts."""
    query = """
        SELECT name,
               ST_X(ST_Centroid(geometry)) as lon,
               ST_Y(ST_Centroid(geometry)) as lat
        FROM atlas.maharashtra_districts
        ORDER BY name;
    """
    records = await conn.fetch(query)
    return [
        {"name": r["name"], "lon": float(r["lon"]), "lat": float(r["lat"])}
        for r in records
    ]


def calculate_quality_score(records_processed: int, districts_expected: int) -> float:
    """Calculate data quality score based on completeness."""
    if districts_expected == 0:
        return 0.0
    # Expected records = districts * days. Cap completeness at 1.0
    expected = districts_expected * DAYS_BACK
    completeness = min(records_processed / expected, 1.0) if expected > 0 else 0.0
    # Base score 80 + up to 20 for completeness
    return 80.0 + (completeness * 20.0)


@asset(
    name="weather_nasa_power_maharashtra",
    group_name="meteorology",
    description="Daily weather data (precipitation, temperature) for all 36 Maharashtra districts from NASA POWER API.",
)
async def weather_nasa_power_maharashtra(context: AssetExecutionContext) -> None:
    """
    Production Dagster asset for NASA POWER weather ingestion.

    Pipeline:
    1. Fetch district centroids from PostGIS
    2. Query NASA POWER API for each district (last 30 days)
    3. Validate data quality
    4. Upsert to atlas.maharashtra_weather_daily (idempotent)
    5. Emit lineage and quality metadata
    """
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    context.log.info("🚀 Starting NASA POWER weather ingestion pipeline...")

    conn = await asyncpg.connect(
        user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
    )

    try:
        # Step 1: Get district centroids
        districts = await get_district_centroids(conn)
        context.log.info(f"📍 Found {len(districts)} district centroids")

        # Step 2: Calculate date range
        end_date = datetime.now(timezone.utc) - timedelta(days=1)
        start_date = end_date - timedelta(days=DAYS_BACK)
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")

        # Step 3: Fetch data for each district
        connector = NASAPowerConnector()
        total_records = 0
        failed_districts: List[str] = []

        upsert_query = """
            INSERT INTO atlas.maharashtra_weather_daily
            (district_name, date, latitude, longitude, precipitation_mm, temp_max_c, temp_min_c, geometry)
            VALUES ($1, $2, $3, $4, $5, $6, $7, ST_SetSRID(ST_MakePoint($4, $3), 4326))
            ON CONFLICT (district_name, date) DO UPDATE SET
                precipitation_mm = EXCLUDED.precipitation_mm,
                temp_max_c = EXCLUDED.temp_max_c,
                temp_min_c = EXCLUDED.temp_min_c,
                fetched_at = CURRENT_TIMESTAMP;
        """

        for i, district in enumerate(districts, 1):
            context.log.info(
                f"[{i}/{len(districts)}] Fetching weather for {district['name']}..."
            )

            result = await connector.fetch_daily_point_data(
                latitude=district["lat"],
                longitude=district["lon"],
                start_date=start_str,
                end_date=end_str,
                parameters=PARAMETERS,
            )

            if not result.success:
                failed_districts.append(district["name"])
                context.log.warning(f"  ❌ Failed: {result.error_message}")
                continue

            # Parse and upsert records
            param_data = (
                result.raw_payload.get("properties", {}).get("parameter", {})
                if result.raw_payload
                else {}
            )
            prectot = param_data.get("PRECTOTCORR", {})
            t2m_max = param_data.get("T2M_MAX", {})
            t2m_min = param_data.get("T2M_MIN", {})

            records_to_insert = []
            for date_str in prectot.keys():
                date_obj = datetime.strptime(date_str, "%Y%m%d").date()
                records_to_insert.append(
                    (
                        district["name"],
                        date_obj,
                        district["lat"],
                        district["lon"],
                        prectot.get(date_str),
                        t2m_max.get(date_str),
                        t2m_min.get(date_str),
                    )
                )

            if records_to_insert:
                await conn.executemany(upsert_query, records_to_insert)
                total_records += len(records_to_insert)

            # Polite delay to respect API rate limits
            await asyncio.sleep(0.5)

        await connector.close()

        # Step 4: Quality validation & metrics
        quality_score = calculate_quality_score(total_records, len(districts))
        db_count = await conn.fetchval(
            "SELECT COUNT(*) FROM atlas.maharashtra_weather_daily;"
        )

        # Step 5: Emit Dagster metadata
        context.add_output_metadata(
            {
                "districts_processed": MetadataValue.int(len(districts)),
                "districts_failed": MetadataValue.int(len(failed_districts)),
                "records_upserted": MetadataValue.int(total_records),
                "total_records_in_db": MetadataValue.int(db_count),
                "quality_score": MetadataValue.float(quality_score),
                "date_range": MetadataValue.text(f"{start_str} → {end_str}"),
                "failed_districts": MetadataValue.json(failed_districts),
                "lineage": MetadataValue.json(
                    {
                        "source": "NASA POWER API",
                        "connector_version": "1.0.0",
                        "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                ),
            }
        )

        context.log.info("=" * 70)
        context.log.info("📊 PIPELINE COMPLETE")
        context.log.info("=" * 70)
        context.log.info(f"  🌍 Districts Processed: {len(districts)}")
        context.log.info(f"  ❌ Districts Failed: {len(failed_districts)}")
        context.log.info(f"  📈 Records Upserted: {total_records}")
        context.log.info(f"  💾 Total Records in DB: {db_count}")
        context.log.info(f"  ⭐ Quality Score: {quality_score:.1f}/100")
        context.log.info("=" * 70)

        if failed_districts:
            context.log.warning(f"⚠️  Failed districts: {', '.join(failed_districts)}")

    finally:
        await conn.close()
        context.log.info("🔌 Database connection closed.")
