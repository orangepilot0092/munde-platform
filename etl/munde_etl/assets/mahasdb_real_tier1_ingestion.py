"""
MahaSDB / Real Tier 1 Data Ingestion Assets (NO SIMULATED DATA)
"""
import pandas as pd
from uuid import uuid4
from dagster import asset, get_dagster_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from munde.core.models import IntelligenceAsset
from munde.data_connectors.real_sources.imd_connector import IMDConnector
from munde.data_connectors.real_sources.cpcb_connector import CPCBConnector
from munde.data_connectors.real_sources.census_connector import CensusConnector
from munde.data_connectors.real_sources.bhuvan_connector import BhuvanConnector
from munde.data_connectors.real_sources.ogd_connector import OGDConnector

logger = get_dagster_logger()
DB_URL = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"

def _ingest_to_db(asset_name_prefix: str, df: pd.DataFrame, quality_score: float, owner: str, domain: str, source_url: str):
    if df.empty:
        logger.warning(f"⚠️ No real data fetched for {asset_name_prefix}. Skipping ingestion.")
        return 0
    
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    count = 0
    with Session() as session:
        for _, row in df.iterrows():
            city_or_district = row.get('city') or row.get('district')
            asset_name = f"{asset_name_prefix}: {city_or_district} ({row.get('date', 'N/A')}) [REAL]"
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

@asset(name="ogd_agmarknet_maharashtra_real", description="REAL OGD Agmarknet data", group_name="maharashtra_data_atlas", tags={"domain": "agriculture", "tier": "1"})
def ingest_real_ogd_agmarknet() -> dict:
    connector = OGDConnector(api_key="579b464db66ec23bdd00000103e5864391664f595bd47834ed7abef7")
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("OGD Market", clean_df, score, "Dept. of Agriculture", "agriculture", "https://data.gov.in/"), "status": "success" if not clean_df.empty else "skipped"}

@asset(name="imd_weather_maharashtra_real", description="REAL IMD Weather data", group_name="maharashtra_data_atlas", tags={"domain": "weather", "tier": "1"})
def ingest_real_imd_weather() -> dict:
    connector = IMDConnector()
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("IMD Weather", clean_df, score, "India Meteorological Department", "weather", "https://open-meteo.com/"), "status": "success" if not clean_df.empty else "skipped"}

@asset(name="cpcb_aqi_maharashtra_real", description="REAL CPCB Air Quality data", group_name="maharashtra_data_atlas", tags={"domain": "environment", "tier": "1"})
def ingest_real_cpcb_aqi() -> dict:
    connector = CPCBConnector()
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("CPCB AQI", clean_df, score, "Central Pollution Control Board", "environment", "https://openaq.org/"), "status": "success" if not clean_df.empty else "skipped"}

@asset(name="census_maharashtra_real", description="REAL Census data", group_name="maharashtra_data_atlas", tags={"domain": "demographics", "tier": "1"})
def ingest_real_census() -> dict:
    connector = CensusConnector()
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("Census", clean_df, score, "Census of India", "demographics", "https://censusindia.gov.in/"), "status": "success" if not clean_df.empty else "skipped"}

@asset(name="bhuvan_landcover_maharashtra_real", description="REAL ISRO Bhuvan data", group_name="maharashtra_data_atlas", tags={"domain": "geospatial", "tier": "1"})
def ingest_real_bhuvan_landcover() -> dict:
    connector = BhuvanConnector()
    clean_df, score = connector.validate(connector.normalize(connector.fetch()))
    return {"records_processed": _ingest_to_db("Bhuvan Land Cover", clean_df, score, "ISRO NRSC", "geospatial", "https://bhuvan.nrsc.gov.in/"), "status": "success" if not clean_df.empty else "skipped"}
