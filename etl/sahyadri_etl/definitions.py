from dagster import Definitions

from etl.sahyadri_etl.assets.crop_production import ingest_crop_production_metadata
from etl.sahyadri_etl.assets.document_processing import process_sample_government_report
from etl.sahyadri_etl.assets.embeddings import generate_metadata_embeddings
from etl.sahyadri_etl.assets.raw_ingestion import ingest_crop_production_raw_data

defs = Definitions(
    assets=[
        ingest_crop_production_metadata,
        ingest_crop_production_raw_data,
        generate_metadata_embeddings,
        process_sample_government_report,
    ],
)
