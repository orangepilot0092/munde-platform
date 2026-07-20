"""
Ingest biodiversity and agricultural occurrence data from GBIF API for Maharashtra.
"""

import asyncio
import logging
import os
from datetime import datetime

try:
    import asyncpg
except ImportError:
    print("❌ asyncpg not found. Install via: poetry add asyncpg")
    exit(1)

from src.data_atlas.connectors.gbif import GBIFConnector

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def ingest_gbif_data():
    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    logger.info("🚀 Starting Maharashtra GBIF biodiversity data ingestion...")

    try:
        # 1. Connect to PostGIS
        conn = await asyncpg.connect(
            user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
        )
        logger.info("✅ Connected to PostgreSQL.")

        # 2. Ensure target table exists
        await conn.execute("CREATE SCHEMA IF NOT EXISTS atlas;")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS atlas.maharashtra_biodiversity_occurrences (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                gbif_id VARCHAR(100) UNIQUE NOT NULL,
                species_name VARCHAR(255),
                common_name VARCHAR(255),
                kingdom VARCHAR(100),
                occurrence_date DATE,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                basis_of_record VARCHAR(100),
                geometry GEOMETRY(Point, 4326),
                source VARCHAR(100) DEFAULT 'GBIF API',
                tier VARCHAR(50) DEFAULT 'Tier 1 - Fully Open',
                fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_gbif_geometry ON atlas.maharashtra_biodiversity_occurrences USING GIST (geometry);"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_gbif_species ON atlas.maharashtra_biodiversity_occurrences (species_name);"
        )
        logger.info(
            "📊 Target table 'atlas.maharashtra_biodiversity_occurrences' is ready."
        )

        # 3. Fetch data from GBIF
        connector = GBIFConnector()
        data = await connector.search_occurrences(
            country="IN", state_province="Maharashtra", limit=500
        )

        results = data.get("results", [])
        logger.info(f"📥 Received {len(results)} occurrence records from GBIF.")

        # 4. Transform and prepare records
        records_to_insert = []
        for item in results:
            gbif_id = item.get("key")
            species = item.get("scientificName", "Unknown")
            common = item.get("vernacularName")
            kingdom = item.get("kingdom")
            lat = item.get("decimalLatitude")
            lon = item.get("decimalLongitude")
            basis = item.get("basisOfRecord")

            # Parse date if available
            date_str = item.get("eventDate")
            occ_date = None
            if date_str:
                try:
                    # GBIF dates can be just year, year-month, or full ISO. We'll take the first 10 chars.
                    occ_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
                except ValueError:
                    occ_date = None

            if gbif_id and lat and lon:
                records_to_insert.append(
                    (
                        str(gbif_id),
                        str(species),
                        str(common) if common else None,
                        str(kingdom) if kingdom else None,
                        occ_date,
                        float(lat),
                        float(lon),
                        str(basis) if basis else None,
                    )
                )

        logger.info(
            f"🎯 Prepared {len(records_to_insert)} valid geolocated records for upsert."
        )

        # 5. Upsert into database
        if records_to_insert:
            upsert_query = """
                INSERT INTO atlas.maharashtra_biodiversity_occurrences 
                (gbif_id, species_name, common_name, kingdom, occurrence_date, 
                 latitude, longitude, basis_of_record, geometry)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, ST_SetSRID(ST_MakePoint($7, $6), 4326))
                ON CONFLICT (gbif_id) DO UPDATE SET
                    species_name = EXCLUDED.species_name,
                    common_name = EXCLUDED.common_name,
                    occurrence_date = EXCLUDED.occurrence_date,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    basis_of_record = EXCLUDED.basis_of_record,
                    geometry = EXCLUDED.geometry,
                    fetched_at = CURRENT_TIMESTAMP;
            """
            await conn.executemany(upsert_query, records_to_insert)
            logger.info(
                f"✅ Successfully upserted {len(records_to_insert)} occurrence records."
            )

        # 6. Summary
        db_count = await conn.fetchval(
            "SELECT COUNT(*) FROM atlas.maharashtra_biodiversity_occurrences;"
        )
        logger.info("\n" + "=" * 70)
        logger.info("📊 INGESTION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"  🌿 Total Records Fetched: {len(results)}")
        logger.info(f"  📈 Valid Records Upserted: {len(records_to_insert)}")
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
    asyncio.run(ingest_gbif_data())
