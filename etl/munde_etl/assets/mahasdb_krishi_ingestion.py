"""
MahaSDB / Krishi Data Ingestion Asset
Ingests, validates, and registers LIVE agricultural data as an Intelligence Asset.
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from munde.core.models import IntelligenceAsset
from munde.data_connectors.krishi_live import fetch_live_krishi_telemetry

logger = get_dagster_logger()

@asset(
    name="krishi_agri_advisory_maharashtra_live",
    description="Ingests LIVE telemetry data for crop advisories and soil health across Maharashtra",
    group_name="maharashtra_data_atlas",
    tags={"domain": "agriculture", "source": "krishi_live_telemetry", "owner": "agriculture_department"}
)
def ingest_live_krishi_data() -> dict:
    logger.info("🚀 Starting LIVE Krishi Agricultural Data ingestion pipeline...")
    
    # 1. EXTRACT
    live_data = fetch_live_krishi_telemetry()
    df = pd.DataFrame(live_data)
    logger.info(f"✅ Extracted {len(df)} LIVE agricultural records.")

    # 2. TRANSFORM & VALIDATE
    required_fields = ["district", "taluka", "crop", "soil_moisture_percent", "advisory", "date"]
    completeness = sum(1 for field in required_fields if field in df.columns and df[field].notna().all())
    quality_score = round((completeness / len(required_fields)) * 100, 2)
    logger.info(f"📊 Data validation complete. Quality Score: {quality_score}%")

    # 3. LOAD
    db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        for _, row in df.iterrows():
            asset_name = f"Krishi: {row['crop']} Advisory in {row['taluka']}, {row['district']} ({row['date']}) [LIVE]"
            
            exists = session.query(IntelligenceAsset).filter(IntelligenceAsset.name == asset_name).first()
            
            if not exists:
                asset_record = IntelligenceAsset(
                    id=uuid4(),
                    name=asset_name,
                    description=f"LIVE advisory for {row['crop']} in {row['taluka']}, {row['district']}. Soil moisture: {row['soil_moisture_percent']}%. Market price: ₹{row['market_price_per_quintal']}/quintal. Advisory: {row['advisory']}",
                    owner_department="Department of Agriculture, Govt. of Maharashtra",
                    domain="agriculture",
                    quality_score=quality_score,
                    is_verified=True,
                    source_url=row["source_url"],
                    version="1.0.0"
                )
                session.add(asset_record)
                logger.info(f"💾 Ingested LIVE agri asset: {row['crop']} in {row['district']}")
        
        session.commit()

    return {"records_processed": len(df), "quality_score": quality_score, "status": "success", "is_live": True}
