from src.data_atlas.models import DatasetMetadata
from datetime import datetime
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class DataQualityService:
    """Calculates quality scores for datasets based on standardized criteria."""

    @staticmethod
    def calculate_freshness(last_updated: datetime) -> float:
        if not last_updated:
            return 1.0
        delta = datetime.now() - last_updated
        days = delta.days
        if days < 7:
            return 5.0
        elif days < 30:
            return 4.0
        elif days < 90:
            return 3.0
        elif days < 365:
            return 2.0
        else:
            return 1.0

    @staticmethod
    def calculate_machine_readability(fmt: str) -> float:
        machine_readable = ["JSON", "CSV", "XML", "GeoJSON", "GTFS", "Parquet"]
        if fmt.upper() in machine_readable:
            return 5.0
        elif fmt.upper() in ["XLSX", "PDF"]:
            return 2.0
        else:
            return 1.0

    @staticmethod
    def calculate_completeness(meta: DatasetMetadata) -> float:
        score = 0
        total = 5
        if meta.description:
            score += 1
        if meta.department:
            score += 1
        if meta.source_url:
            score += 1
        if meta.license != "Unknown":
            score += 1
        if meta.tags:
            score += 1
        return (score / total) * 5

    def assess_quality(self, meta: DatasetMetadata) -> dict:
        freshness = self.calculate_freshness(meta.last_updated)
        readability = self.calculate_machine_readability(meta.format)
        completeness = self.calculate_completeness(meta)

        # Weighted average: Freshness (30%), Readability (30%), Completeness (40%)
        overall = (freshness * 0.3) + (readability * 0.3) + (completeness * 0.4)

        return {
            "overall": round(overall, 2),
            "freshness": freshness,
            "completeness": completeness,
            "machine_readability": readability,
        }
