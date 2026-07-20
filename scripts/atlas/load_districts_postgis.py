"""
Load Maharashtra Districts GeoJSON into PostGIS.
Creates the 'atlas.maharashtra_districts' table and upserts all 36 districts.
"""

import asyncio
import json
import logging
import os
from pathlib import Path

try:
    import asyncpg
except ImportError:
    print("❌ asyncpg not found. Install it via: poetry add asyncpg")
    exit(1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    geojson_path = Path("data/osm/maharashtra_districts.geojson")
    if not geojson_path.exists():
        logger.error(f"GeoJSON file not found at {geojson_path}")
        return

    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])
    logger.info(f"📂 Loaded {len(features)} districts from GeoJSON")

    # Database connection parameters (matches your dev.yml defaults)
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv(
        "DB_HOST", "localhost"
    )  # Use 'postgres' if running inside docker network

    logger.info(f"🔌 Connecting to PostgreSQL at {db_host}:5432 as {db_user}...")

    try:
        conn = await asyncpg.connect(
            user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
        )
        logger.info("✅ Connected successfully.")

        # 1. Enable PostGIS extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

        # 2. Ensure 'atlas' schema exists
        await conn.execute("CREATE SCHEMA IF NOT EXISTS atlas;")

        # 3. Create the districts table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS atlas.maharashtra_districts (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(100) UNIQUE NOT NULL,
                name_en VARCHAR(100),
                name_mr VARCHAR(100),
                admin_level INT,
                ref_lgd_district VARCHAR(50),
                source VARCHAR(100),
                tier VARCHAR(50),
                geometry GEOMETRY(MultiPolygon, 4326),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        logger.info("📊 Table 'atlas.maharashtra_districts' is ready.")

        # 4. Upsert data
        insert_query = """
            INSERT INTO atlas.maharashtra_districts 
            (name, name_en, name_mr, admin_level, ref_lgd_district, source, tier, geometry)
            VALUES ($1, $2, $3, $4, $5, $6, $7, ST_Multi(ST_GeomFromGeoJSON($8)))
            ON CONFLICT (name) DO UPDATE SET
                name_en = EXCLUDED.name_en,
                name_mr = EXCLUDED.name_mr,
                admin_level = EXCLUDED.admin_level,
                ref_lgd_district = EXCLUDED.ref_lgd_district,
                source = EXCLUDED.source,
                tier = EXCLUDED.tier,
                geometry = EXCLUDED.geometry,
                updated_at = CURRENT_TIMESTAMP;
        """

        success_count = 0
        for feature in features:
            props = feature.get("properties", {})
            geom = json.dumps(feature.get("geometry"))

            await conn.execute(
                insert_query,
                props.get("name"),
                props.get("name_en"),
                props.get("name_mr"),
                int(props.get("admin_level", 5)) if props.get("admin_level") else 5,
                props.get("ref_lgd_district"),
                props.get("source", "OpenStreetMap Nominatim"),
                props.get("tier", "Tier 1"),
                geom,
            )
            success_count += 1

        logger.info(f"✅ Successfully upserted {success_count} districts into PostGIS.")

        # 5. Verify count
        count = await conn.fetchval("SELECT COUNT(*) FROM atlas.maharashtra_districts;")
        logger.info(f"📊 Total districts currently in database: {count}")

    except asyncpg.exceptions.CannotConnectNowError:
        logger.error(
            "❌ Cannot connect to database. Is PostgreSQL running and accessible on localhost:5432?"
        )
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
    finally:
        if "conn" in locals():
            await conn.close()
            logger.info("🔌 Database connection closed.")


if __name__ == "__main__":
    asyncio.run(main())
