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
        "resource_id": "84d26d02-935b-479c-9427-c27ee1afd76f",
        "dataset_name": "District-wise Forest Cover - Maharashtra (2011 Assessment)",
        "domain": "Environment",
        "department": "NITI Aayog / FSI",
        "source": "Data.gov.in",
        "license": "Government Open Data License (GODL)",
        "refresh_frequency": "Historical (superseded by ISRO SFR 2021/2023)",
        "last_updated": "2014-04-17",
        "geographic_resolution": "District-level (35 districts)",
        "priority": "medium-high",
        "schema_fields": [
            "District",
            "Geographical_Area_SqKm",
            "VDF_SqKm",
            "MDF_SqKm",
            "Open_Forest_SqKm",
            "Total_Forest_SqKm",
            "Percent_of_GA",
            "Change_SqKm",
            "Scrub_SqKm",
        ],
        "data_snapshot": {
            "state_total_forest_pct": 16.46,
            "highest_cover_district": {"name": "Gadchiroli", "pct": 70.04},
            "lowest_cover_district": {"name": "Latur", "pct": 0.07},
            "max_loss_district": {"name": "Sindhudurg", "change_sqkm": -5},
            "max_gain_district": {"name": "Chandrapur", "change_sqkm": 4},
            "total_scrub_sqkm": 4157,
            "districts_count": 35,
        },
        "ai_readiness": [
            "Historical Baseline for Change Detection",
            "Deforestation Hotspot Classification",
            "Afforestation Target Identification (Scrub Land)",
            "Spatial Join with KG Administrative Entities",
            "Water Stress Correlation Analysis (JalSetu)",
            "Carbon Stock Estimation Baseline",
        ],
        "quality_scores": {
            "freshness": 2,
            "completeness": 5,
            "accuracy": 4,
            "machine_readability": 5,
            "geographic_resolution": 4,
            "overall": 4.0,
        },
        "recommended_complement": "ISRO/NRSC State of Forest Report 2021/2023 via Bhuvan WMS",
        "complement_api_id": "api_bhuvan_wms",
        "paryavaran_mapping": {
            "use_cases": [
                "District forest cover dashboard",
                "Deforestation alert baseline comparison",
                "Scrub-to-forest conversion targeting",
                "Biodiversity hotspot identification",
            ]
        },
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
        "ds_forest_cover_district_mh_2011",
        "District-wise Forest Cover MH 2011 (Baseline)",
        "Environment",
        "https://api.data.gov.in/resource/84d26d02-935b-479c-9427-c27ee1afd76f",
        metadata,
    ),
)

conn.commit()
cur.close()
conn.close()
print(
    "✅ Cataloged District-wise Forest Cover MH 2011 as MEDIUM-HIGH priority baseline"
)
