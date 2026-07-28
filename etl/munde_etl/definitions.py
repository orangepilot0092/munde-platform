from dagster import Definitions, load_assets_from_modules
from etl.munde_etl.assets import (
    mahasdb_real_tier1_ingestion,
    mahasdb_tier2_ingestion,
    mahasdb_municipal_ingestion,
    mahasdb_tier4_ingestion # <-- NEW TIER 4 CONNECTORS
)

all_assets = load_assets_from_modules([
    mahasdb_real_tier1_ingestion,
    mahasdb_tier2_ingestion,
    mahasdb_municipal_ingestion,
    mahasdb_tier4_ingestion
])

defs = Definitions(assets=all_assets)
