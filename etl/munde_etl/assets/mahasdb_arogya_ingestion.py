"""
MahaSDB / Arogya Data Ingestion Asset
Ingests, validates, and registers LIVE health infrastructure data as an Intelligence Asset.
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from munde.core.models import IntelligenceAsset
from munde.data_connectors.arogya_live import fetch_live_arogya_telemetry

logger = get_dagster_logger()

@asset(
    name="arogya_health_infrastructure_maharashtra_live",
    description="Ingests LIVE telemetry data for PHC/CHC capacity and health advisories across Maharashtra",
    group_name="maharashtra_data_atlas",
    tags={"domain": "health", "source": "arogya_live_telemetry", "owner": "public_health_department"}
)
def ingest_live_arogya_data() -> dict:
    logger.info("🚀 Starting LIVE Arogya Health Data ingestion pipeline...")
    
    # 1. EXTRACT
    live_data = fetch_live_arogya_telemetry()
    df = pd.DataFrame(live_data)
    logger.info(f"✅ Extracted {len(df)} LIVE health records.")

    # 2. TRANSFORM & VALIDATE
    required_fields = ["district", "taluka", "facility", "available_beds", "advisory", "date"]
    completeness = sum(1 for field in required_fields if field in df.columns and df[field].notna().all())
    quality_score = round((completeness / len(required_fields)) * 100, 2)
    logger.info(f"📊 Data validation complete. Quality Score: {quality_score}%")

    # 3. LOAD
    db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        for _, row in df.iterrows():
            asset_name = f"Arogya: {row['facility']} Status in {row['taluka']}, {row['district']} ({row['date']}) [LIVE]"
            
            exists = session.query(IntelligenceAsset).filter(IntelligenceAsset.name == asset_name).first()
            
            if not exists:
                asset_record = IntelligenceAsset(
                    id=uuid4(),
                    name=asset_name,
                    description=f"LIVE health advisory for {row['facility']} in {row['taluka']}, {row['district']}. Total Beds: {row['total_beds']}, Available: {row['available_beds']} ({row['occupancy_percent']}% occupancy). Advisory: {row['advisory']}. Emergency: {row['emergency_contact']}",
                    owner_department="Department of Public Health, Govt. of Maharashtra",
                    domain="health",
                    quality_score=quality_score,
                    is_verified=True,
                    source_url=row["source_url"],
                    version="1.0.0"
                )
                session.add(asset_record)
                logger.info(f"💾 Ingested LIVE health asset: {row['facility']} in {row['district']}")
        
        session.commit()

    return {"records_processed": len(df), "quality_score": quality_score, "status": "success", "is_live": True}
