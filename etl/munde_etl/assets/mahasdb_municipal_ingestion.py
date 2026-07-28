"""
MahaSDB / Tier 3 Data Ingestion Asset
Ingests REAL Municipal Corporation civic data (Hospitals, Schools, Waste, Water).
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from munde.core.models import IntelligenceAsset
from munde.data_connectors.real_sources.municipal_connector import MunicipalConnector

logger = get_dagster_logger()
DB_URL = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"

def _ingest_to_db(asset_prefix: str, df: pd.DataFrame, quality_score: float, owner: str, domain: str, source_url: str) -> int:
    if df.empty:
        logger.warning(f"⚠️ No real Tier 3 data fetched for {asset_prefix}. Skipping ingestion.")
        return 0
    
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    count = 0
    with Session() as session:
        for _, row in df.iterrows():
            asset_name = f"Municipal: {row['facility_type']} - {row['name']} in {row['city']} ({row['date']}) [REAL]"
            if not session.query(IntelligenceAsset).filter(IntelligenceAsset.name == asset_name).first():
                session.add(IntelligenceAsset(
                    id=uuid4(), name=asset_name,
                    description=f"REAL civic data for {row['corporation']}. Facility: {row['name']} ({row['facility_type']}). Ward: {row['ward']}. Status: {row['status']}.",
                    owner_department=owner, domain=domain, quality_score=quality_score, is_verified=True,
                    source_url=source_url, version="1.0.0"
                ))
                count += 1
        session.commit()
    return count

@asset(name="municipal_civic_data_maharashtra_real", description="REAL Municipal Corporation civic infrastructure data", group_name="maharashtra_data_atlas", tags={"domain": "civic", "tier": "3"})
def ingest_real_municipal_data() -> dict:
    logger.info("🚀 Starting REAL Municipal Civic Data ingestion...")
    connector = MunicipalConnector()
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {
        "records_processed": _ingest_to_db("Municipal Civic", clean_df, score, "Various Municipal Corporations, Govt of Maharashtra", "civic", "https://data.gov.in/"), 
        "status": "success" if not clean_df.empty else "skipped"
    }
