"""
Ingest daily weather data from NASA POWER API for all 36 Maharashtra districts.
Fetches district centroids from PostGIS, queries NASA POWER, and upserts the results.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

try:
    import asyncpg
except ImportError:
    print("❌ asyncpg not found. Install via: poetry add asyncpg")
    exit(1)

from src.data_atlas.connectors.nasa_power import NASAPowerConnector

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PARAMETERS = ["PRECTOTCORR", "T2M_MAX", "T2M_MIN"]
DAYS_BACK = 30


async def get_district_centroids(conn) -> List[Dict[str, Any]]:
    """Fetch name and centroid coordinates of all districts."""
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


async def ingest_weather_data():
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    logger.info("🚀 Starting Maharashtra-wide NASA POWER weather ingestion...")

    try:
        # 1. Connect to PostGIS
        conn = await asyncpg.connect(
            user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
        )
        logger.info("✅ Connected to PostgreSQL.")

        # 2. Ensure target table exists
        await conn.execute("CREATE SCHEMA IF NOT EXISTS atlas;")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS atlas.maharashtra_weather_daily (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                district_name VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                precipitation_mm FLOAT,
                temp_max_c FLOAT,
                temp_min_c FLOAT,
                geometry GEOMETRY(Point, 4326),
                source VARCHAR(100) DEFAULT 'NASA POWER API',
                tier VARCHAR(50) DEFAULT 'Tier 1 - Fully Open',
                fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (district_name, date)
            );
        """)
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_weather_district_date ON atlas.maharashtra_weather_daily (district_name, date);"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_weather_geometry ON atlas.maharashtra_weather_daily USING GIST (geometry);"
        )
        logger.info("📊 Target table 'atlas.maharashtra_weather_daily' is ready.")

        # 3. Get district centroids
        districts = await get_district_centroids(conn)
        logger.info(f"📍 Found {len(districts)} district centroids to process.")

        # 4. Calculate date range
        end_date = datetime.now(timezone.utc) - timedelta(days=1)
        start_date = end_date - timedelta(days=DAYS_BACK)
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")

        connector = NASAPowerConnector()
        total_records = 0

        # 5. Fetch and upsert for each district
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
            logger.info(
                f"[{i}/{len(districts)}] Fetching weather for {district['name']}..."
            )

            try:
                data = await connector.fetch_daily_point_data(
                    latitude=district["lat"],
                    longitude=district["lon"],
                    start_date=start_str,
                    end_date=end_str,
                    parameters=PARAMETERS,
                )

                param_data = data.get("properties", {}).get("parameter", {})
                # NASA POWER returns dates as direct keys: {"PRECTOTCORR": {"20260601": 0.5, ...}}
                prectot = param_data.get("PRECTOTCORR", {})
                t2m_max = param_data.get("T2M_MAX", {})
                t2m_min = param_data.get("T2M_MIN", {})

                # Use PRECTOTCORR dates as the canonical date list
                date_keys = list(prectot.keys())

                records_to_insert = []
                for date_str in date_keys:
                    # Parse date string (YYYYMMDD) to DATE object
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
                    # Use copy_records_to_db or executemany for efficiency
                    await conn.executemany(upsert_query, records_to_insert)
                    total_records += len(records_to_insert)
                    logger.info(
                        f"  ✅ {district['name']}: {len(records_to_insert)} days upserted."
                    )

                # Polite delay to respect NASA POWER API rate limits
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"  ❌ Failed for {district['name']}: {e}")

        # 6. Summary
        db_count = await conn.fetchval(
            "SELECT COUNT(*) FROM atlas.maharashtra_weather_daily;"
        )
        logger.info("\n" + "=" * 70)
        logger.info("📊 INGESTION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"  🌍 Districts Processed: {len(districts)}")
        logger.info(f"  📅 Days per District: {DAYS_BACK}")
        logger.info(f"  📈 Total Records Upserted: {total_records}")
        logger.info(f"  💾 Total Records in DB: {db_count}")
        logger.info("=" * 70)

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        if "conn" in locals():
            await conn.close()
            logger.info("🔌 Database connection closed.")


if __name__ == "__main__":
    asyncio.run(ingest_weather_data())
