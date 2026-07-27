"""
MahaSDB / WRD Data Ingestion Asset
Ingests, validates, and registers LIVE water resource data as an Intelligence Asset.
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from munde.core.models import Base, IntelligenceAsset
from munde.data_connectors.wrd_live import fetch_live_reservoir_telemetry

logger = get_dagster_logger()

@asset(
    name="wrd_reservoir_levels_maharashtra_live",
    description="Ingests LIVE telemetry data from Maharashtra WRD reservoirs",
    group_name="maharashtra_data_atlas",
    tags={"domain": "water", "source": "wrd_live_telemetry", "owner": "water_resources_department"}
)
def ingest_live_wrd_reservoir_data() -> dict:
    logger.info("🚀 Starting LIVE WRD Reservoir Data ingestion pipeline...")
    
    # 1. EXTRACT: Fetch LIVE telemetry data
    live_data = fetch_live_reservoir_telemetry()
    df = pd.DataFrame(live_data)
    logger.info(f"✅ Extracted {len(df)} LIVE records from WRD IoT sensors.")

    # 2. TRANSFORM & VALIDATE
    required_fields = ["reservoir_name", "district", "capacity_mcm", "current_storage_mcm", "date"]
    completeness = sum(1 for field in required_fields if field in df.columns and df[field].notna().all())
    quality_score = round((completeness / len(required_fields)) * 100, 2)
    logger.info(f"📊 Data validation complete. Quality Score: {quality_score}%")

    # 3. LOAD: Upsert into PostgreSQL
    db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        for _, row in df.iterrows():
            # Check if asset already exists for today to avoid duplicates
            exists = session.query(IntelligenceAsset).filter(
                IntelligenceAsset.name.ilike(f"WRD: {row['reservoir_name']} Reservoir Level ({row['date']})")
            ).first()
            
            if not exists:
                asset_record = IntelligenceAsset(
                    id=uuid4(),
                    name=f"WRD: {row['reservoir_name']} Reservoir Level ({row['date']}) [LIVE]",
                    description=f"LIVE telemetry for {row['reservoir_name']} in {row['district']}. Current storage: {row['current_storage_mcm']} MCM ({row['utilization_percent']}% of {row['capacity_mcm']} MCM capacity). Live inflow: {row['inflow_mcm']} MCM.",
                    owner_department="Water Resources Department, Govt. of Maharashtra",
                    domain="water",
                    quality_score=quality_score,
                    is_verified=True,
                    source_url=row["source_url"],
                    version="1.0.0"
                )
                session.add(asset_record)
                logger.info(f"💾 Ingested LIVE asset: {row['reservoir_name']}")
        
        session.commit()

    return {"records_processed": len(df), "quality_score": quality_score, "status": "success", "is_live": True}
