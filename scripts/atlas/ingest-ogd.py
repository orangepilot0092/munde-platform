#!/usr/bin/env python3
"""Script to ingest metadata into Sahyadri Data Atlas Registry."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.data_atlas.connectors.mock import MockMaharashtraConnector
from src.data_atlas.registry import MetadataRegistry
from src.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.logging import get_logger

logger = get_logger(__name__)


def main():
    logger.info("Starting Maharashtra Data Atlas Ingestion (Registry Mode)...")

    # Setup DB Connection
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        connector = MockMaharashtraConnector()
        registry = MetadataRegistry(db)

        datasets = connector.discover_datasets()
        logger.info(f"Discovered {len(datasets)} datasets.")

        for meta in datasets:
            registry.save_dataset(meta)

        logger.info("Ingestion complete. Metadata saved to PostgreSQL.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
