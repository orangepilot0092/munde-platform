from dagster import asset
from src.data_atlas.connectors.mock import MockMaharashtraConnector
from src.data_atlas.registry import MetadataRegistry
from src.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@asset
def ingest_crop_production_metadata():
    """Ingests metadata for Maharashtra Crop Production dataset."""
    connector = MockMaharashtraConnector()

    # Setup DB Connection for Registry
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        registry = MetadataRegistry(db)
        datasets = connector.discover_datasets()

        # Filter for agriculture domain for this specific asset
        agri_datasets = [d for d in datasets if d.domain == "Agriculture"]

        for meta in agri_datasets:
            registry.save_dataset(meta)

        return {"status": "success", "count": len(agri_datasets)}
    finally:
        db.close()
