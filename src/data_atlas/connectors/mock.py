from typing import List
from src.data_atlas.connectors.base import BaseConnector
from src.data_atlas.models import DatasetMetadata
from src.core.logging_config import get_logger
from datetime import datetime

logger = get_logger(__name__)


class MockMaharashtraConnector(BaseConnector):
    """Mock connector for testing the Data Atlas framework."""

    def __init__(self):
        super().__init__("Mock Maharashtra Data")

    def discover_datasets(self) -> List[DatasetMetadata]:
        """Return a list of sample datasets for Maharashtra."""
        logger.info("Generating mock dataset metadata...")

        datasets = [
            DatasetMetadata(
                dataset_id="maha_agri_001",
                name="Maharashtra District-wise Crop Production",
                description="Annual crop production statistics for major crops across Maharashtra districts.",
                domain="Agriculture",
                department="Department of Agriculture, Maharashtra",
                source_url="https://maharashtra.gov.in/agriculture",
                license="Open Government License",
                format="CSV",
                refresh_frequency="Annual",
                last_updated=datetime.now(),
                quality_score=4.5,
                tags=["crops", "production", "districts"],
            ),
            DatasetMetadata(
                dataset_id="maha_water_001",
                name="Major Reservoir Levels in Maharashtra",
                description="Daily water storage levels in major reservoirs across the state.",
                domain="Water Resources",
                department="Water Resources Department",
                source_url="https://mahawater.gov.in",
                license="Open Government License",
                format="JSON",
                refresh_frequency="Daily",
                last_updated=datetime.now(),
                quality_score=4.8,
                tags=["water", "reservoirs", "levels"],
            ),
            DatasetMetadata(
                dataset_id="maha_transport_001",
                name="MSRTC Bus Routes and Schedules",
                description="Complete list of MSRTC bus routes, stops, and scheduled timings.",
                domain="Transport",
                department="MSRTC",
                source_url="https://msrtc.gov.in",
                license="Open Government License",
                format="GTFS",
                refresh_frequency="Monthly",
                last_updated=datetime.now(),
                quality_score=3.9,
                tags=["transport", "bus", "routes"],
            ),
        ]

        return datasets

    def ingest_data(self, dataset_id: str) -> bool:
        """Simulate data ingestion."""
        logger.info(f"Simulating ingestion for dataset: {dataset_id}")
        return True
