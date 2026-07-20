import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from psycopg2.extras import Json
from src.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()

metadata = Json(
    {
        "resource_id": "TO_BE_EXTRACTED_FROM_API_TAB",
        "dataset_name": "Land Use Pattern - Maharashtra",
        "domain": "Land Intelligence",
        "department": "NITI Aayog",
        "source": "Data.gov.in",
        "license": "Government Open Data License (GODL)",
        "refresh_frequency": "Annual",
        "last_updated": "2025-06-02",
        "geographic_resolution": "State-level aggregate",
        "priority": "high",
        "schema_fields": ["Land_Use_Category", "Area_Thousands_Ha", "Percentage"],
        "data_snapshot": {
            "total_geographical_area_ha": 30771000,
            "net_area_sown_pct": 56.66,
            "forest_cover_pct": 16.95,
            "culturable_wasteland_pct": 2.98,
            "current_fallows_pct": 4.45,
            "permanent_pastures_pct": 4.05,
        },
        "ai_readiness": [
            "Land Use Classification Baseline",
            "Crop Planning Context for KrishiSetu",
            "Water Stress Modeling Input for JalSetu",
            "RAG Ground Truth for BhoomiSetu Queries",
        ],
        "recommended_complement": "MRSAC LULC (district/taluka level) via Bhuvan WMS",
        "complement_api_id": "api_bhuvan_wms",
        "verified_date": "2026-07-09",
    }
)

cur.execute(
    """
    INSERT INTO metadata_registry (dataset_id, name, domain, source_url, metadata)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (dataset_id) DO UPDATE SET metadata = EXCLUDED.metadata
""",
    (
        "ds_land_use_pattern_mh",
        "Land Use Pattern - Maharashtra (Baseline)",
        "Land Intelligence",
        "https://data.gov.in/catalog/land-use-pattern-maharashtra",
        metadata,
    ),
)

conn.commit()
cur.close()
conn.close()
print("✅ Cataloged Land Use Pattern MH as HIGH PRIORITY baseline dataset")
