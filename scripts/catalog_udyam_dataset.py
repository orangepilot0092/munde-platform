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
        "resource_id": "8b68ae56-84cf-4728-a0a6-1be11028dea7",
        "dataset_name": "List of MSME Registered Units under UDYAM",
        "domain": "Industry",
        "department": "Ministry of MSME",
        "source": "Data.gov.in",
        "license": "Government Open Data License (GODL)",
        "refresh_frequency": "Daily",
        "last_updated": "2026-07-08",
        "total_records_national": 41546353,
        "maharashtra_filter": {"field": "LG_ST_Code", "value": "27"},
        "schema_fields": [
            "Activities",
            "CommunicationAddress",
            "District",
            "EnterpriseName",
            "LG_DT_Code",
            "LG_ST_Code",
            "Pincode",
            "RegistrationDate",
            "State",
        ],
        "ai_readiness": [
            "Clustering",
            "Classification",
            "Geospatial Analytics",
            "Recommendation Systems",
        ],
        "key_finding": "Use LG_ST_Code (numeric) for state filtering. State names are UPPERCASE.",
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
        "ds_udyam_msme_mh",
        "UDYAM MSME Registration (Maharashtra)",
        "Industry",
        "https://api.data.gov.in/resource/8b68ae56-84cf-4728-a0a6-1be11028dea7",
        metadata,
    ),
)

conn.commit()
cur.close()
conn.close()
print("✅ Cataloged UDYAM MSME dataset in metadata_registry")
