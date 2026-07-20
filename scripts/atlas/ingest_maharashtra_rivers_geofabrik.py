"""
Ingest Maharashtra river and canal network from Geofabrik India OSM extract.
Uses direct PBF download (no API timeouts) and filters for waterways within Maharashtra.
"""

import asyncio
import logging
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any

try:
    import asyncpg
    import httpx
except ImportError:
    print("❌ Missing dependencies. Install via: poetry add asyncpg httpx")
    exit(1)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Geofabrik India extract URL (updated weekly, stable)
GEOFABRIK_INDIA_URL = "https://download.geofabrik.de/asia/india-latest.osm.pbf"

# Maharashtra bounding box (approximate)
MH_BBOX = {"south": 15.5, "north": 22.1, "west": 72.5, "east": 81.0}


async def download_geofabrik_extract(output_path: Path) -> bool:
    """Download the latest India OSM extract from Geofabrik."""
    if output_path.exists():
        logger.info(f"✅ Using cached Geofabrik extract: {output_path}")
        return True

    logger.info("📥 Downloading India OSM extract from Geofabrik (~400MB)...")
    logger.info(f"   URL: {GEOFABRIK_INDIA_URL}")

    try:
        async with httpx.AsyncClient(timeout=600.0, follow_redirects=True) as client:
            async with client.stream("GET", GEOFABRIK_INDIA_URL) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length", 0))

                with open(output_path, "wb") as f:
                    downloaded = 0
                    async for chunk in response.aiter_bytes(
                        chunk_size=1024 * 1024
                    ):  # 1MB chunks
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            pct = (downloaded / total) * 100
                            if int(pct) % 10 == 0:
                                logger.info(
                                    f"   Progress: {pct:.1f}% ({downloaded // (1024 * 1024)}MB / {total // (1024 * 1024)}MB)"
                                )

        logger.info(
            f"✅ Download complete: {output_path} ({output_path.stat().st_size // (1024 * 1024)}MB)"
        )
        return True

    except Exception as e:
        logger.error(f"❌ Download failed: {e}")
        return False


def extract_maharashtra_waterways(
    pbf_path: Path, output_geojson: Path
) -> List[Dict[str, Any]]:
    """
    Extract named waterways within Maharashtra bounding box from PBF.
    Uses osmium or ogr2ogr if available, falls back to manual parsing.
    """
    # Check if osmium tool is available
    try:
        result = subprocess.run(["osmium", "--version"], capture_output=True, text=True)
        has_osmium = result.returncode == 0
    except FileNotFoundError:
        has_osmium = False

    if has_osmium:
        logger.info("🔧 Using osmium to extract waterways...")
        # Use osmium to filter for waterways in Maharashtra bbox
        temp_filtered = pbf_path.parent / "mh_waterways.osm.pbf"

        bbox_filter = (
            f"{MH_BBOX['west']},{MH_BBOX['south']},{MH_BBOX['east']},{MH_BBOX['north']}"
        )

        # Extract ways with waterway tag in bbox
        cmd = [
            "osmium",
            "extract",
            "--overwrite",
            "-b",
            bbox_filter,
            "-s",
            "complete_ways",
            "-o",
            str(temp_filtered),
            str(pbf_path),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"✅ Extracted Maharashtra bbox to: {temp_filtered}")

            # Now filter for waterway features and convert to GeoJSON
            cmd2 = [
                "osmium",
                "tags-filter",
                "--overwrite",
                str(temp_filtered),
                "w/waterway=river,canal",
                "-o",
                str(output_geojson).replace(".geojson", ".osm.pbf"),
            ]
            subprocess.run(cmd2, check=True, capture_output=True)

            # Convert to GeoJSON using ogr2ogr if available
            try:
                cmd3 = [
                    "ogr2ogr",
                    "-f",
                    "GeoJSON",
                    str(output_geojson),
                    str(output_geojson).replace(".geojson", ".osm.pbf"),
                ]
                subprocess.run(cmd3, check=True, capture_output=True)
                logger.info(f"✅ Converted to GeoJSON: {output_geojson}")
            except (FileNotFoundError, subprocess.CalledProcessError):
                logger.warning("⚠️ ogr2ogr not available. Using Python fallback parser.")
                return parse_pbf_manually(temp_filtered)

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ osmium failed: {e.stderr.decode()}")
            return []

    # Fallback: Use Python to parse PBF (slower but works without external tools)
    logger.info("🔧 Using Python PBF parser (osmium Python library or manual)...")
    return parse_pbf_manually(pbf_path)


def parse_pbf_manually(pbf_path: Path) -> List[Dict[str, Any]]:
    """
    Manual PBF parsing fallback using the osmium Python library.
    """
    try:
        import osmium

        class WaterwayHandler(osmium.SimpleHandler):
            def __init__(self):
                super().__init__()
                self.features = []

            def way(self, w):
                # Check if it's a named waterway
                if w.tags.get("waterway") in ("river", "canal") and w.tags.get("name"):
                    # Check if within Maharashtra bbox
                    nodes = list(w.nodes)
                    if not nodes:
                        return

                    lats = [n.lat for n in nodes if n.location.valid()]
                    lons = [n.lon for n in nodes if n.location.valid()]

                    if not lats or not lons:
                        return

                    # Simple bbox check: if any node is in MH, include it
                    in_mh = any(
                        MH_BBOX["south"] <= lat <= MH_BBOX["north"]
                        and MH_BBOX["west"] <= lon <= MH_BBOX["east"]
                        for lat, lon in zip(lats, lons)
                    )

                    if in_mh:
                        # Calculate centroid
                        center_lat = sum(lats) / len(lats)
                        center_lon = sum(lons) / len(lons)

                        self.features.append(
                            {
                                "osm_id": w.id,
                                "name": w.tags.get("name"),
                                "name_mr": w.tags.get("name:mr", ""),
                                "waterway_type": w.tags.get("waterway"),
                                "latitude": center_lat,
                                "longitude": center_lon,
                            }
                        )

        handler = WaterwayHandler()
        logger.info(
            "🔍 Parsing PBF file (this may take 1-2 minutes for full India extract)..."
        )
        handler.apply_file(str(pbf_path), locations=True)

        logger.info(f"✅ Found {len(handler.features)} named waterways in Maharashtra")
        return handler.features

    except ImportError:
        logger.error("❌ Neither osmium CLI nor Python library available.")
        logger.info("💡 Install osmium tools: sudo apt-get install osmium-tool")
        logger.info("💡 Or install Python library: pip install osmium")
        return []


async def load_to_postgis(waterways: List[Dict[str, Any]]):
    """Load extracted waterways into PostGIS."""
    if not waterways:
        logger.warning("⚠️ No waterways to load.")
        return

    db_user = os.getenv("DB_USER", "sahyadri")
    db_pass = os.getenv("DB_PASSWORD", "sahyadri_secret")
    db_name = os.getenv("DB_NAME", "sahyadri_db")
    db_host = os.getenv("DB_HOST", "localhost")

    conn = await asyncpg.connect(
        user=db_user, password=db_pass, database=db_name, host=db_host, port=5432
    )
    logger.info("✅ Connected to PostgreSQL for river data upsert.")

    await conn.execute("CREATE SCHEMA IF NOT EXISTS atlas;")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS atlas.maharashtra_rivers (
            osm_id BIGINT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            name_mr VARCHAR(255),
            waterway_type VARCHAR(100),
            latitude FLOAT,
            longitude FLOAT,
            geometry GEOMETRY(Point, 4326),
            source VARCHAR(100) DEFAULT 'OpenStreetMap (Geofabrik)',
            tier VARCHAR(50) DEFAULT 'Tier 1 - Fully Open',
            fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    await conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_rivers_geometry ON atlas.maharashtra_rivers USING GIST (geometry);"
    )
    await conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_rivers_name ON atlas.maharashtra_rivers (name);"
    )
    logger.info("📊 Target table 'atlas.maharashtra_rivers' is ready.")

    upsert_query = """
        INSERT INTO atlas.maharashtra_rivers 
        (osm_id, name, name_mr, waterway_type, latitude, longitude, geometry)
        VALUES ($1, $2, $3, $4, $5, $6, ST_SetSRID(ST_MakePoint($6, $5), 4326))
        ON CONFLICT (osm_id) DO UPDATE SET
            name = EXCLUDED.name,
            name_mr = EXCLUDED.name_mr,
            waterway_type = EXCLUDED.waterway_type,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            geometry = EXCLUDED.geometry,
            fetched_at = CURRENT_TIMESTAMP;
    """

    for w in waterways:
        await conn.execute(
            upsert_query,
            w["osm_id"],
            w["name"],
            w["name_mr"],
            w["waterway_type"],
            w["latitude"],
            w["longitude"],
        )

    db_count = await conn.fetchval("SELECT COUNT(*) FROM atlas.maharashtra_rivers;")
    logger.info(
        f"✅ Successfully upserted {len(waterways)} river/canal centroids into PostGIS."
    )
    logger.info(f"💾 Total river segments in DB: {db_count}")

    await conn.close()


async def main():
    data_dir = Path("data/geofabrik")
    data_dir.mkdir(parents=True, exist_ok=True)

    pbf_path = data_dir / "india-latest.osm.pbf"

    logger.info("🚀 Starting Maharashtra river network ingestion from Geofabrik...")

    # Step 1: Download India extract
    if not await download_geofabrik_extract(pbf_path):
        logger.error("❌ Failed to download Geofabrik extract. Aborting.")
        return

    # Step 2: Extract Maharashtra waterways
    logger.info("🔍 Extracting named waterways within Maharashtra bounding box...")
    waterways = extract_maharashtra_waterways(pbf_path, data_dir / "mh_rivers.geojson")

    if not waterways:
        logger.error("❌ No waterways extracted. Check if osmium tools are installed.")
        logger.info("💡 Quick fix: sudo apt-get install osmium-tool python3-osmium")
        return

    # Step 3: Load to PostGIS
    await load_to_postgis(waterways)

    logger.info("\n" + "=" * 70)
    logger.info("📊 INGESTION SUMMARY")
    logger.info("=" * 70)
    logger.info(f"  🌊 Waterways Extracted: {len(waterways)}")
    logger.info("  📁 Source: Geofabrik India Extract (direct download, no API)")
    logger.info("  🗺️  Filter: Maharashtra bounding box + named rivers/canals")
    logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
