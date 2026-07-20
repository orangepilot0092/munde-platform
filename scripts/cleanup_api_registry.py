import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from src.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()

# Remove old duplicate entries that lack auth_config_ref
old_duplicates = [
    "api_data_gov_in_odata",
    "api_imd_forecast",
    "api_mahabhulekh_ror",
    "api_cpcb_aqi",
    "api_epfo_uan",
    "api_fssai_license",
    "api_gst_system",
    "api_india_post_tracking",
    "api_pincode_india",
    "api_maha_rera",
    "api_mca_charges",
    "api_msrtc_gtfs",
    "api_ngt_orders",
    "api_parivahan_sarathi",
    "api_parivahan_vahan",
    "api_supreme_court",
]

placeholders = ",".join(["%s"] * len(old_duplicates))
cur.execute(
    f"DELETE FROM api_registry WHERE api_id IN ({placeholders})", old_duplicates
)
deleted = cur.rowcount

# Ensure remaining entries have correct access_status
cur.execute("""
    UPDATE api_registry SET access_status = 'open' 
    WHERE api_id IN ('api_osm_overpass') AND access_status != 'open'
""")

conn.commit()
cur.close()
conn.close()
print(f"✅ Cleaned up {deleted} duplicate/outdated API registry entries")
