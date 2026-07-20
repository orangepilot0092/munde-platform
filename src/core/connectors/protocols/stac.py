"""
STAC (SpatioTemporal Asset Catalog) Connector Protocol.
Extends BaseConnector to query Earth Observation data (e.g., Microsoft Planetary Computer).
"""

import logging
import time
from typing import Any, List

from src.core.connectors.base import BaseConnector, IngestionResult, LineageMetadata

logger = logging.getLogger(__name__)


class STACConnector(BaseConnector):
    """
    Connector for STAC APIs.
    """

    def __init__(
        self,
        name: str,
        catalog_url: str,
        version: str = "1.0.0",
        timeout: float = 60.0,
        max_retries: int = 3,
    ):
        super().__init__(
            name=name, version=version, timeout=timeout, max_retries=max_retries
        )
        self.catalog_url = catalog_url

    async def search_items(
        self,
        collections: List[str],
        bbox: List[float],
        datetime_range: str,
        limit: int = 10,
    ) -> IngestionResult:
        """
        Search a STAC catalog for items matching criteria.
        """
        start_time = time.time()
        endpoint = f"{self.catalog_url}/search"

        lineage = LineageMetadata(
            source_system=self.name,
            source_url=endpoint,
            connector_version=self.version,
            filters_applied={
                "collections": collections,
                "bbox": bbox,
                "datetime": datetime_range,
            },
        )

        payload = {
            "collections": collections,
            "bbox": bbox,
            "datetime": datetime_range,
            "limit": limit,
        }

        try:
            response = await self._request_with_retry("POST", endpoint, json=payload)
            data = response.json()

            features = data.get("features", [])
            lineage.record_count = len(features)
            lineage.extraction_duration_ms = int((time.time() - start_time) * 1000)

            return IngestionResult(
                success=True,
                records_processed=len(features),
                quality_score=95.0,
                lineage=lineage,
                raw_payload={
                    "features_count": len(features),
                    "sample_ids": [f.get("id") for f in features[:5]],
                },
            )

        except Exception as e:
            logger.error(f"[{self.name}] STAC search failed: {e}")
            lineage.extraction_duration_ms = int((time.time() - start_time) * 1000)
            return IngestionResult(
                success=False,
                quality_score=0.0,
                lineage=lineage,
                error_message=str(e),
            )

    async def fetch(self, *args: Any, **kwargs: Any) -> IngestionResult:
        return await self.search_items(*args, **kwargs)
