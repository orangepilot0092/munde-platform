from sqlalchemy.orm import Session
from sqlalchemy import text
from src.data_atlas.models import DatasetMetadata
from src.core.logging_config import get_logger
from src.data_atlas.quality import DataQualityService
import json

logger = get_logger(__name__)


class MetadataRegistry:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.qs = DataQualityService()

    def save_dataset(self, meta: DatasetMetadata, storage_path: str = None):
        """Save or update a dataset in the metadata_registry."""
        quality_scores = self.qs.assess_quality(meta)

        query = text("""
            INSERT INTO metadata_registry 
            (dataset_id, name, description, domain, department, source_url, license, format, 
             refresh_frequency, last_updated, quality_score, freshness_score, completeness_score, 
             machine_readability_score, tags, storage_path)
            VALUES 
            (:dataset_id, :name, :description, :domain, :department, :source_url, :license, :format,
             :refresh_frequency, :last_updated, :quality_score, :freshness_score, :completeness_score,
             :machine_readability_score, :tags, :storage_path)
            ON CONFLICT (dataset_id) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                quality_score = EXCLUDED.quality_score,
                last_updated = EXCLUDED.last_updated,
                storage_path = EXCLUDED.storage_path
        """)

        self.db.execute(
            query,
            {
                "dataset_id": meta.dataset_id,
                "name": meta.name,
                "description": meta.description,
                "domain": meta.domain,
                "department": meta.department,
                "source_url": meta.source_url,
                "license": meta.license,
                "format": meta.format,
                "refresh_frequency": meta.refresh_frequency,
                "last_updated": meta.last_updated,
                "quality_score": quality_scores["overall"],
                "freshness_score": quality_scores["freshness"],
                "completeness_score": quality_scores["completeness"],
                "machine_readability_score": quality_scores["machine_readability"],
                "tags": json.dumps(meta.tags),
                "storage_path": storage_path,
            },
        )
        self.db.commit()
        logger.info(
            f"Saved metadata for {meta.dataset_id} with storage path {storage_path}"
        )
