"""
MahaSDB / Tier 4 Data Ingestion Assets
Ingests REAL Geocoding and PIN Code utility data.
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from munde.core.models import IntelligenceAsset
from munde.data_connectors.real_sources.geocoding_connector import GeocodingConnector
from munde.data_connectors.real_sources.pincode_connector import PincodeConnector

logger = get_dagster_logger()
DB_URL = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"

def _ingest_to_db(asset_prefix: str, df: pd.DataFrame, quality_score: float, owner: str, domain: str, source_url: str) -> int:
    if df.empty:
        logger.warning(f"⚠️ No real Tier 4 data fetched for {asset_prefix}. Skipping ingestion.")
        return 0
    
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    count = 0
    with Session() as session:
        for _, row in df.iterrows():
            loc = row.get('city') or row.get('district') or row.get('post_office')
            asset_name = f"Tier4: {asset_prefix} - {loc} ({row.get('date', 'N/A')}) [REAL]"
            if not session.query(IntelligenceAsset).filter(IntelligenceAsset.name == asset_name).first():
                session.add(IntelligenceAsset(
                    id=uuid4(), name=asset_name,
                    description=str(row.to_dict()),
                    owner_department=owner, domain=domain, quality_score=quality_score, is_verified=True,
                    source_url=source_url, version="1.0.0"
                ))
                count += 1
        session.commit()
    return count

@asset(name="geocoding_pune_coords_real", description="REAL Reverse Geocoding for Pune coordinates", group_name="maharashtra_data_atlas", tags={"domain": "utility", "tier": "4"})
def ingest_real_geocoding() -> dict:
    logger.info("🚀 Starting REAL Geocoding Data ingestion...")
    # Example: Coordinates for Shivaji Nagar, Pune
    connector = GeocodingConnector(query_type="reverse", lat=18.5304, lon=73.8567)
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("Reverse Geocode", clean_df, score, "OpenStreetMap Contributors", "utility", "https://nominatim.openstreetmap.org/"), "status": "success" if not clean_df.empty else "skipped"}

@asset(name="pincode_411001_real", description="REAL PIN Code lookup for 411001 (Pune)", group_name="maharashtra_data_atlas", tags={"domain": "utility", "tier": "4"})
def ingest_real_pincode() -> dict:
    logger.info("🚀 Starting REAL PIN Code Data ingestion...")
    connector = PincodeConnector(pincode="411001")
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("PIN Code 411001", clean_df, score, "India Post", "utility", "https://api.postalpincode.in/"), "status": "success" if not clean_df.empty else "skipped"}
