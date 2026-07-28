"""
MahaSDB / Bhumi Data Ingestion Asset
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from munde.core.models import IntelligenceAsset
from munde.data_connectors.bhumi_live import fetch_live_bhumi_telemetry

logger = get_dagster_logger()

@asset(
    name="bhumi_land_intelligence_maharashtra_live",
    description="Ingests LIVE telemetry data for land records, 7/12 extracts, and soil health",
    group_name="maharashtra_data_atlas",
    tags={"domain": "land", "source": "bhumi_live_telemetry", "owner": "revenue_department"}
)
def ingest_live_bhumi_data() -> dict:
    logger.info("🚀 Starting LIVE Bhumi Land Data ingestion pipeline...")
    live_data = fetch_live_bhumi_telemetry()
    df = pd.DataFrame(live_data)
    
    db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        for _, row in df.iterrows():
            asset_name = f"Bhumi: Survey {row['survey_no']} in {row['village']}, {row['taluka']} ({row['date']}) [LIVE]"
            if not session.query(IntelligenceAsset).filter(IntelligenceAsset.name == asset_name).first():
                asset_record = IntelligenceAsset(
                    id=uuid4(), name=asset_name,
                    description=f"LIVE land record for Survey No. {row['survey_no']} in {row['village']}, {row['taluka']}, {row['district']}. Land Use: {row['land_use']}. Soil: {row['soil_type']}. Area: {row['area_hectares']} Ha. Status: {row['status']}.",
                    owner_department="Department of Revenue, Govt. of Maharashtra",
                    domain="land", quality_score=100.0, is_verified=True,
                    source_url=row["source_url"], version="1.0.0"
                )
                session.add(asset_record)
        session.commit()
    return {"records_processed": len(df), "status": "success"}
