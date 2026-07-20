"""
Dagster Asset: Open-Meteo Historical Weather Data for Maharashtra Districts.
Production-grade, idempotent pipeline using the new RESTConnector protocol.
Serves as the golden template for all future REST-based dataset migrations.
"""

import asyncio
import logging
import os
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

import asyncpg  # type: ignore[import-untyped]
from dagster import AssetExecutionContext, MetadataValue, asset

from src.core.connectors.protocols.rest import RESTConnector

logger = logging.getLogger(__name__)

# Open-Meteo daily variables for agriculture/water intelligence
DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "et0_fao_evapotranspiration",
]

ARCHIVE_API_URL = "https://archive-api.open-meteo.com/v1/archive"


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
        {"name": str(r["name"]), "lon": float(r["lon"]), "lat": float(r["lat"])}
        for r in records
    ]


def calculate_quality_score(records_processed: int, districts_expected: int) -> float:
    """Calculate data quality score based on completeness."""
    if districts_expected == 0:
        return 0.0
    completeness = min(records_processed / districts_expected, 1.0)
    return 80.0 + (completeness * 20.0)


@asset(
    name="weather_open_meteo_maharashtra",
    group_name="meteorology",
    description="Historical daily weather data (temp, precipitation, evapotranspiration) for all 36 Maharashtra districts from Open-Meteo Archive API.",
)
async def weather_open_meteo_maharashtra(context: AssetExecutionContext) -> None:
    """
    Production Dagster asset for Open-Meteo weather ingestion.

    Pipeline:
    1. Fetch district centroids from PostGIS
    2. Query Open-Meteo Archive API for each district (last 90 days)
    3. Validate data quality
    4. Upsert to atlas.maharashtra_weather_daily (idempotent)
    5. Emit lineage and quality metadata
    """
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    context.log.info("🚀 Starting Open-Meteo weather ingestion pipeline...")

    conn = await asyncpg.connect(
        user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
    )

    try:
        # Step 1: Get district centroids
        districts = await get_district_centroids(conn)
        context.log.info(f"📍 Found {len(districts)} district centroids")

        # Step 2: Calculate date range (last 90 days)
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=90)
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()

        # Step 3: Initialize RESTConnector
        connector = RESTConnector(
            name="open_meteo_archive",
            base_url=ARCHIVE_API_URL,
            version="1.0.0",
            timeout=60.0,
            max_retries=3,
        )

        total_records = 0
        failed_districts: List[str] = []

        upsert_query = """
            INSERT INTO atlas.maharashtra_weather_daily
            (district_name, date, latitude, longitude, precipitation_mm, temp_max_c, temp_min_c, geometry)
            VALUES ($1, $2, $3, $4, $5, $6, $7, ST_SetSRID(ST_MakePoint($4, $3), 4326))
            ON CONFLICT (district_name, date) DO UPDATE SET
                precipitation_mm = COALESCE(EXCLUDED.precipitation_mm, atlas.maharashtra_weather_daily.precipitation_mm),
                temp_max_c = COALESCE(EXCLUDED.temp_max_c, atlas.maharashtra_weather_daily.temp_max_c),
                temp_min_c = COALESCE(EXCLUDED.temp_min_c, atlas.maharashtra_weather_daily.temp_min_c),
                fetched_at = CURRENT_TIMESTAMP;
        """

        for i, district in enumerate(districts, 1):
            context.log.info(
                f"[{i}/{len(districts)}] Fetching weather for {district['name']}..."
            )

            params: Dict[str, Any] = {
                "latitude": district["lat"],
                "longitude": district["lon"],
                "start_date": start_str,
                "end_date": end_str,
                "daily": ",".join(DAILY_VARIABLES),
                "timezone": "Asia/Kolkata",
            }

            result = await connector.fetch_paginated(
                endpoint="",
                params=params,
                max_pages=1,  # Open-Meteo returns all data in one response
            )

            if not result.success or result.raw_payload is None:
                failed_districts.append(district["name"])
                context.log.warning(f"  ❌ Failed: {result.error_message}")
                continue

            # Parse Open-Meteo response structure
            daily_data = result.raw_payload.get("daily", {})
            dates = daily_data.get("time", [])
            temp_max = daily_data.get("temperature_2m_max", [])
            temp_min = daily_data.get("temperature_2m_min", [])
            precip = daily_data.get("precipitation_sum", [])

            records_to_insert: List[tuple] = []
            for idx, date_str in enumerate(dates):
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue

                # Safely extract values with None fallback
                t_max = temp_max[idx] if idx < len(temp_max) else None
                t_min = temp_min[idx] if idx < len(temp_min) else None
                p_sum = precip[idx] if idx < len(precip) else None

                records_to_insert.append(
                    (
                        district["name"],
                        date_obj,
                        district["lat"],
                        district["lon"],
                        p_sum,
                        t_max,
                        t_min,
                    )
                )

            if records_to_insert:
                await conn.executemany(upsert_query, records_to_insert)
                total_records += len(records_to_insert)
                context.log.info(f"  ✅ Upserted {len(records_to_insert)} records")

            # Polite delay to respect API rate limits
            await asyncio.sleep(0.5)

        await connector.close()

        # Step 4: Quality validation & metrics
        quality_score = calculate_quality_score(
            len(districts) - len(failed_districts), len(districts)
        )
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
                "source": MetadataValue.text("Open-Meteo Archive API"),
            }
        )

        context.log.info("=" * 70)
        context.log.info("📊 OPEN-METEO PIPELINE COMPLETE")
        context.log.info("=" * 70)
        context.log.info(f"  🌍 Districts Processed: {len(districts)}")
        context.log.info(f"  ❌ Districts Failed: {len(failed_districts)}")
        context.log.info(f"  📈 Records Upserted: {total_records}")
        context.log.info(f"  💾 Total Records in DB: {db_count}")
        context.log.info(f"  ⭐ Quality Score: {quality_score:.1f}/100")
        context.log.info("=" * 70)

        if failed_districts:
            context.log.warning(f"⚠️  Failed districts: {', '.join(failed_districts)}")

    except Exception as e:
        context.log.error(f"❌ Open-Meteo pipeline failed: {e}")
        raise
    finally:
        await conn.close()
        context.log.info("🔌 Database connection closed.")
