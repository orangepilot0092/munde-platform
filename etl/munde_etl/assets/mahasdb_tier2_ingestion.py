"""
MahaSDB / Tier 2 Data Ingestion Assets
Ingests REAL WRD and Soil Health data from Maharashtra Government Portals.
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from munde.core.models import IntelligenceAsset
from munde.data_connectors.real_sources.wrd_real_connector import WRDRealConnector
from munde.data_connectors.real_sources.soil_health_connector import SoilHealthConnector

logger = get_dagster_logger()
DB_URL = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"

def _ingest_to_db(asset_prefix: str, df: pd.DataFrame, quality_score: float, owner: str, domain: str, source_url: str) -> int:
    if df.empty:
        logger.warning(f"⚠️ No real Tier 2 data fetched for {asset_prefix}. Skipping ingestion.")
        return 0
    
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    count = 0
    with Session() as session:
        for _, row in df.iterrows():
            loc = row.get('reservoir') or row.get('taluka')
            dist = row.get('district')
            asset_name = f"{asset_prefix}: {loc}, {dist} ({row.get('date', 'N/A')}) [REAL]"
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

@asset(name="wrd_reservoir_levels_maharashtra_real", description="REAL WRD daily reservoir levels via portal scraping", group_name="maharashtra_data_atlas", tags={"domain": "water", "tier": "2"})
def ingest_real_wrd_levels() -> dict:
    logger.info("🚀 Starting REAL WRD Data ingestion...")
    connector = WRDRealConnector()
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("WRD Reservoir", clean_df, score, "Water Resources Dept, Govt of Maharashtra", "water", "https://wrd.maharashtra.gov.in/"), "status": "success" if not clean_df.empty else "skipped"}

@asset(name="soil_health_maharashtra_real", description="REAL Soil Health Card data for Maharashtra", group_name="maharashtra_data_atlas", tags={"domain": "agriculture", "tier": "2"})
def ingest_real_soil_health() -> dict:
    logger.info("🚀 Starting REAL Soil Health Data ingestion...")
    connector = SoilHealthConnector()
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("Soil Health", clean_df, score, "Dept of Agriculture, Govt of Maharashtra", "agriculture", "https://soilhealth.dac.gov.in/"), "status": "success" if not clean_df.empty else "skipped"}
