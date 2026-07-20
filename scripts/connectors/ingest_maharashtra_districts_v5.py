"""
Ingest all Maharashtra district boundaries using Nominatim API.
V5: Uses Nominatim for direct, reliable GeoJSON boundary fetching, avoiding Overpass timeouts.
"""

import asyncio
import json
import logging
import httpx
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Official district names to query
MAHARASHTRA_DISTRICTS = [
    "Ahilyanagari",
    "Akola",
    "Amravati",
    "Beed",
    "Bhandara",
    "Buldhana",
    "Chandrapur",
    "Chhatrapati Sambhajinagar",
    "Dharashiv",
    "Dhule",
    "Gadchiroli",
    "Gondia",
    "Hingoli",
    "Jalgaon",
    "Jalna",
    "Kolhapur",
    "Latur",
    "Mumbai City",
    "Mumbai Suburban",
    "Nagpur",
    "Nanded",
    "Nandurbar",
    "Nashik",
    "Palghar",
    "Parbhani",
    "Pune",
    "Raigad",
    "Ratnagiri",
    "Sangli",
    "Satara",
    "Sindhudurg",
    "Solapur",
    "Thane",
    "Wardha",
    "Washim",
    "Yavatmal",
]

# Fallback names if the primary name fails (e.g., old names still in OSM)
DISTRICT_FALLBACKS = {
    "Ahilyanagari": "Ahmednagar",
    "Chhatrapati Sambhajinagar": "Aurangabad",
    "Dharashiv": "Osmanabad",
    "Mumbai City": "Mumbai",
    "Mumbai Suburban": "Mumbai Suburban",
}


async def fetch_district_from_nominatim(
    session: httpx.AsyncClient, district_name: str
) -> Optional[Dict[str, Any]]:
    """Fetch a district boundary from Nominatim API."""
    # Query format: "Pune district, Maharashtra, India"
    query = f"{district_name} district, Maharashtra, India"
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "format": "geojson",
        "q": query,
        "polygon_geojson": 1,
        "limit": 1,
        "accept-language": "en,mr",
    }

    headers = {
        "User-Agent": "ProjectSahyadri/1.0 (https://sahyadri.ai; advait@sahyadri.ai)"
    }

    try:
        response = await session.get(url, params=params, headers=headers, timeout=30.0)
        response.raise_for_status()
        data = response.json()

        if data.get("features"):
            return data["features"][0]
        return None
    except httpx.HTTPStatusError as e:
        logger.warning(f"HTTP error for {district_name}: {e.response.status_code}")
        return None
    except Exception as e:
        logger.warning(f"Error fetching {district_name}: {e}")
        return None


async def main() -> None:
    output_dir = Path("data/osm")
    output_dir.mkdir(parents=True, exist_ok=True)

    all_features: List[Dict[str, Any]] = []
    successful: List[str] = []
    failed: List[str] = []

    logger.info("🚀 Starting Maharashtra district boundary ingestion (V5 - Nominatim)")
    logger.info("=" * 70)
    logger.info(f"📋 Total districts to process: {len(MAHARASHTRA_DISTRICTS)}")

    # Use a single HTTPX client with connection pooling
    async with httpx.AsyncClient() as session:
        for i, district in enumerate(MAHARASHTRA_DISTRICTS, 1):
            logger.info(f"[{i}/{len(MAHARASHTRA_DISTRICTS)}] Fetching {district}...")

            # Try primary name
            feature = await fetch_district_from_nominatim(session, district)

            # If failed and has a fallback, try fallback
            if not feature and district in DISTRICT_FALLBACKS:
                fallback = DISTRICT_FALLBACKS[district]
                logger.info(f"  ⚠️ Primary name failed. Trying fallback: {fallback}...")
                feature = await fetch_district_from_nominatim(session, fallback)

            if feature:
                # Enrich properties with Sahyadri metadata
                props = feature.get("properties", {})
                feature["properties"] = {
                    "name": props.get("name", district),
                    "name_en": props.get("name:en", district),
                    "name_mr": props.get("name:mr", ""),
                    "name_hi": props.get("name:hi", ""),
                    "admin_level": props.get("admin_level", "5"),
                    "source": "OpenStreetMap Nominatim API",
                    "tier": "Tier 1 - Fully Open",
                    "license": "Open Data Commons Open Database License (ODbL)",
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "osm_id": props.get("osm_id"),
                    "osm_type": props.get("osm_type"),
                }
                all_features.append(feature)
                successful.append(district)
                logger.info(f"  ✅ {district}: Success")
            else:
                failed.append(district)
                logger.error(f"  ❌ {district}: Not found in Nominatim")

            # Nominatim Usage Policy: Max 1 request per second
            await asyncio.sleep(1.1)

    # Sort by name for consistency
    all_features.sort(key=lambda f: f["properties"]["name"])
    successful.sort()

    # Build final GeoJSON
    combined = {
        "type": "FeatureCollection",
        "metadata": {
            "name": "Maharashtra District Boundaries",
            "description": "Administrative boundaries of all 36 districts in Maharashtra",
            "source": "OpenStreetMap Nominatim API",
            "source_url": "https://nominatim.openstreetmap.org/",
            "tier": "Tier 1 - Fully Open",
            "license": "ODbL",
            "total_districts": len(all_features),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "projection": "EPSG:4326 (WGS84)",
            "query_method": "Nominatim Geocoding API with fallback names (V5)",
        },
        "features": all_features,
    }

    # Save files
    output_file = output_dir / "maharashtra_districts.geojson"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    report_file = output_dir / "maharashtra_districts_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total_districts": len(all_features),
                "successful": successful,
                "failed": failed,
                "district_names": [f["properties"]["name"] for f in all_features],
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("📊 INGESTION SUMMARY (V5 - Nominatim)")
    logger.info("=" * 70)
    logger.info(f"  🗺️  Total Districts Found: {len(all_features)}/36")
    logger.info(f"  📁 GeoJSON Saved: {output_file}")
    logger.info(f"  📄 Report Saved: {report_file}")

    if len(all_features) >= 35:
        logger.info("  ✅ SUCCESS: All (or nearly all) 36 districts captured!")
    else:
        logger.info(f"  ⚠️  Found {len(all_features)} districts (expected 36)")
        if failed:
            logger.info(f"  ❌ Missing: {', '.join(failed)}")

    logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
