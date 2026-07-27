"""
Dagster Definitions for Project Munde ETL Pipelines.
Registers all data ingestion assets for the Maharashtra Data Atlas.
"""
from dagster import Definitions, load_assets_from_modules
from etl.munde_etl.assets import mahasdb_wrd_ingestion, mahasdb_krishi_ingestion, mahasdb_arogya_ingestion

# Load all assets from the assets module
all_assets = load_assets_from_modules([mahasdb_wrd_ingestion, mahasdb_krishi_ingestion, mahasdb_arogya_ingestion])

# Define the Dagster repository
defs = Definitions(
    assets=all_assets,
)
