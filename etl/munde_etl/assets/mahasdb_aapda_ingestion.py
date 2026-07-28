"""
MahaSDB / Aapda Data Ingestion Asset
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from munde.core.models import IntelligenceAsset
from munde.data_connectors.aapda_live import fetch_live_aapda_telemetry

logger = get_dagster_logger()

@asset(
    name="aapda_disaster_management_maharashtra_live",
    description="Ingests LIVE telemetry data for disaster alerts, relief camps, and emergency protocols",
    group_name="maharashtra_data_atlas",
    tags={"domain": "disaster", "source": "aapda_live_telemetry", "owner": "state_disaster_management_authority"}
)
def ingest_live_aapda_data() -> dict:
    logger.info("🚀 Starting LIVE Aapda Disaster Data ingestion pipeline...")
    live_data = fetch_live_aapda_telemetry()
    df = pd.DataFrame(live_data)
    
    db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        for _, row in df.iterrows():
            asset_name = f"Aapda: {row['alert_type']} in {row['taluka']}, {row['district']} ({row['date']}) [LIVE]"
            if not session.query(IntelligenceAsset).filter(IntelligenceAsset.name == asset_name).first():
                asset_record = IntelligenceAsset(
                    id=uuid4(), name=asset_name,
                    description=f"LIVE disaster alert for {row['taluka']}, {row['district']}. Type: {row['alert_type']}. Severity: {row['severity']}. Status: {row['status']}. Relief Camps: {row['relief_camps']}. Emergency: {row['emergency_contact']}.",
                    owner_department="State Disaster Management Authority, Govt. of Maharashtra",
                    domain="disaster", quality_score=100.0, is_verified=True,
                    source_url=row["source_url"], version="1.0.0"
                )
                session.add(asset_record)
        session.commit()
    return {"records_processed": len(df), "status": "success"}
