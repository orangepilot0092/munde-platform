"""
MahaSDB / Real OGD Data Ingestion Asset
Ingests, validates, and registers REAL India OGD data as an Intelligence Asset.
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from munde.core.models import IntelligenceAsset
from munde.data_connectors.real_sources.ogd_connector import OGDConnector

logger = get_dagster_logger()

@asset(
    name="ogd_agmarknet_maharashtra_real",
    description="Ingests REAL daily market price data from India OGD (Agmarknet) for Maharashtra",
    group_name="maharashtra_data_atlas",
    tags={"domain": "agriculture", "source": "india_ogd", "tier": "1"}
)
def ingest_real_ogd_agmarknet() -> dict:
    logger.info("🚀 Starting REAL OGD Agmarknet Data ingestion pipeline...")
    
    # 1. Initialize Connector (Replace with your actual data.gov.in API key)
    API_KEY = "579b464db66ec23bdd00000103e5864391664f595bd47834ed7abef7" 
    connector = OGDConnector(api_key=API_KEY)
    
    # 2. FETCH
    raw_df = connector.fetch()
    if raw_df.empty:
        logger.warning("No data fetched from OGD. Skipping ingestion.")
        return {"records_processed": 0, "quality_score": 0.0, "status": "skipped"}
        
    # 3. NORMALIZE & VALIDATE
    normalized_df = connector.normalize(raw_df)
    clean_df, quality_score = connector.validate(normalized_df)
    logger.info(f"📊 Data validation complete. Quality Score: {quality_score}%")
    
    # 4. INGEST
    db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        for _, row in clean_df.iterrows():
            asset_name = f"OGD: {row['crop']} Price in {row['taluka']}, {row['district']} ({row['date']}) [REAL]"
            
            if not session.query(IntelligenceAsset).filter(IntelligenceAsset.name == asset_name).first():
                asset_record = IntelligenceAsset(
                    id=uuid4(),
                    name=asset_name,
                    description=f"REAL market data for {row['crop']} in {row['taluka']}, {row['district']}. Price: ₹{row['market_price_per_quintal']}/quintal.",
                    owner_department="Department of Agriculture, Govt. of Maharashtra (via India OGD)",
                    domain="agriculture",
                    quality_score=quality_score,
                    is_verified=True,
                    source_url=row["source_url"],
                    version="1.0.0"
                )
                session.add(asset_record)
                logger.info(f"💾 Ingested REAL OGD asset: {row['crop']} in {row['district']}")
        
        session.commit()

    return {"records_processed": len(clean_df), "quality_score": quality_score, "status": "success", "is_real": True}
