from abc import ABC, abstractmethod

from src.core.logging_config import get_logger
from src.data_atlas.models import DatasetMetadata

logger = get_logger(__name__)


class BaseConnector(ABC):
    """Abstract base class for all data connectors."""

    def __init__(self, name: str):
        self.name = name
        logger.info(f"Initializing connector: {name}")

    @abstractmethod
    def discover_datasets(self) -> list[DatasetMetadata]:
        """Discover and return metadata for available datasets."""
        pass

    @abstractmethod
    def ingest_data(self, dataset_id: str) -> bool:
        """Ingest raw data for a specific dataset ID."""
        pass

    def validate_connection(self) -> bool:
        """Check if the source is accessible."""
        try:
            # Default implementation; override in subclasses
            return True
        except Exception as e:
            logger.error(f"Connection validation failed for {self.name}: {e}")
            return False
