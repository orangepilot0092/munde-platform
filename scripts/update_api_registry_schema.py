import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from src.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    ALTER TABLE api_registry 
    ADD COLUMN IF NOT EXISTS auth_config_ref VARCHAR(100),
    ADD COLUMN IF NOT EXISTS access_status VARCHAR(50) DEFAULT 'pending',
    ADD COLUMN IF NOT EXISTS application_url TEXT,
    ADD COLUMN IF NOT EXISTS notes TEXT
""")

updates = [
    (
        "api_imd_weather",
        "IMD_API_KEY",
        "open",
        "https://mausam.imd.gov.in/api",
        "Self-service registration at IMD portal",
    ),
    (
        "api_data_gov_in",
        "DATA_GOV_IN_API_KEY",
        "open",
        "https://data.gov.in/user/register",
        "Free instant API key via data.gov.in",
    ),
    (
        "api_bhuvan_wms",
        "BHUVAN_WMS_KEY",
        "open",
        "https://bhuvan-app1.nrsc.gov.in/api/wms",
        "Register at NRSC Bhuvan portal",
    ),
    (
        "api_msamb_apmc",
        "MSAMB_API_KEY",
        "open",
        "https://msamb.com/apmc-api",
        "Contact MSAMB IT cell for API access",
    ),
    (
        "api_osm_overpass",
        None,
        "open",
        "https://wiki.openstreetmap.org/wiki/Overpass_API",
        "No key required. Respect fair use policy.",
    ),
    (
        "api_mahabhulekh",
        "MAHABHULEKH_OAUTH_TOKEN",
        "restricted",
        "https://bhulekh.mahabhumi.gov.in",
        "Requires MoU with Revenue Dept.",
    ),
    (
        "api_mpcb_aqi",
        "MPCB_API_KEY",
        "restricted",
        "https://mpcb.gov.in",
        "Restricted. Apply via RTI or official MoU.",
    ),
    (
        "api_wrd_reservoirs",
        "WRD_API_KEY",
        "restricted",
        "https://wrd.maharashtra.gov.in",
        "Internal dept API. Requires WRD Secretary approval.",
    ),
]

for api_id, config_ref, status, app_url, notes in updates:
    cur.execute(
        """
        UPDATE api_registry 
        SET auth_config_ref = %s, access_status = %s, application_url = %s, notes = %s
        WHERE api_id = %s
    """,
        (config_ref, status, app_url, notes, api_id),
    )

conn.commit()
cur.close()
conn.close()
print("✅ Updated api_registry schema and documentation")
