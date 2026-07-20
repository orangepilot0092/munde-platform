#!/usr/bin/env python3
"""Direct test script for Raw Ingestion and Registry Update."""

import sys
import os
import csv
import tempfile

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.core.storage import MinIOService
from src.data_atlas.registry import MetadataRegistry
from src.data_atlas.connectors.mock import MockMaharashtraConnector
from src.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.logging import get_logger

logger = get_logger(__name__)


def main():
    logger.info("Starting direct raw ingestion test...")

    # 1. Setup DB and Storage
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    storage = MinIOService()

    try:
        # 2. Generate Sample CSV
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".csv", mode="w", newline=""
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["District", "Crop", "Production_Tons"])
            writer.writerow(["Pune", "Wheat", 1500])
            writer.writerow(["Nashik", "Grapes", 2000])
            tmp_path = tmp.name

        logger.info(f"Generated sample data at {tmp_path}")

        # 3. Upload to MinIO
        bucket = "agriculture"
        object_name = "maha_agri_001/sample_data_direct.csv"

        logger.info(f"Uploading to MinIO: {bucket}/{object_name}")
        storage.upload_file(bucket, object_name, tmp_path)
        storage_path = f"s3://{bucket}/{object_name}"

        # 4. Update Registry
        registry = MetadataRegistry(db)
        connector = MockMaharashtraConnector()
        datasets = connector.discover_datasets()
        agri_meta = next((d for d in datasets if d.dataset_id == "maha_agri_001"), None)

        if agri_meta:
            logger.info(
                f"Updating registry for {agri_meta.dataset_id} with path {storage_path}"
            )
            registry.save_dataset(agri_meta, storage_path=storage_path)
        else:
            logger.error("Could not find maha_agri_001 in mock datasets")

        logger.info("✅ Direct ingestion test complete.")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
    finally:
        db.close()
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    main()
