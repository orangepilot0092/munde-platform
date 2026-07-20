from dagster import asset
import os
import tempfile
import csv
from src.core.storage import MinIOService
from src.data_atlas.registry import MetadataRegistry
from src.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data_atlas.connectors.mock import MockMaharashtraConnector


@asset
def ingest_crop_production_raw_data():
    """Generates sample crop production data and stores it in MinIO."""

    # Setup DB and Storage
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    storage = MinIOService()

    try:
        # Generate a simple CSV locally
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".csv", mode="w", newline=""
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["District", "Crop", "Production_Tons"])
            writer.writerow(["Pune", "Wheat", 1500])
            writer.writerow(["Nashik", "Grapes", 2000])
            writer.writerow(["Kolhapur", "Sugar Cane", 5000])
            tmp_path = tmp.name

        # Define MinIO path
        bucket = "agriculture"
        object_name = "maha_agri_001/sample_data.csv"

        # Upload to MinIO
        storage.upload_file(bucket, object_name, tmp_path)
        storage_path = f"s3://{bucket}/{object_name}"

        # Update Registry
        registry = MetadataRegistry(db)
        connector = MockMaharashtraConnector()
        datasets = connector.discover_datasets()
        agri_meta = next((d for d in datasets if d.dataset_id == "maha_agri_001"), None)

        if agri_meta:
            registry.save_dataset(agri_meta, storage_path=storage_path)

        return {"status": "success", "path": storage_path}

    finally:
        db.close()
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
