"""
REST Connector Protocol.
Extends BaseConnector to handle paginated JSON/CSV API responses.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from src.core.connectors.base import BaseConnector, IngestionResult, LineageMetadata

logger = logging.getLogger(__name__)


class RESTConnector(BaseConnector):
    """
    Connector for standard REST APIs returning JSON or CSV.
    Supports pagination and query parameter construction.
    """

    def __init__(
        self,
        name: str,
        base_url: str,
        version: str = "1.0.0",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        super().__init__(
            name=name, version=version, timeout=timeout, max_retries=max_retries
        )
        self.base_url = base_url

    async def fetch_paginated(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        pagination_key: Optional[str] = None,
        max_pages: int = 10,
    ) -> IngestionResult:
        """
        Fetch data from a REST endpoint with optional pagination.
        """
        import time

        start_time = time.time()

        lineage = LineageMetadata(
            source_system=self.name,
            source_url=f"{self.base_url}{endpoint}",
            connector_version=self.version,
            filters_applied=params or {},
        )

        try:
            all_records: List[Dict[str, Any]] = []
            current_params = params.copy() if params else {}
            page = 1

            while page <= max_pages:
                logger.debug(f"[{self.name}] Fetching page {page} from {endpoint}")

                response = await self._request_with_retry(
                    "GET", f"{self.base_url}{endpoint}", params=current_params
                )
                data = response.json()

                # Extract records (handles both list responses and wrapped responses)
                records = (
                    data
                    if isinstance(data, list)
                    else data.get("results", data.get("data", []))
                )

                if not records:
                    break

                all_records.extend(records)
                lineage.record_count = len(all_records)

                # Handle pagination
                if pagination_key and pagination_key in data:
                    current_params[pagination_key] = data[pagination_key]
                elif isinstance(data, dict) and "next" in data and data["next"]:
                    # URL-based pagination (simplified for this example)
                    break
                else:
                    break  # No more pages

                page += 1
                await asyncio.sleep(0.5)  # Polite delay

            lineage.extraction_duration_ms = int((time.time() - start_time) * 1000)

            return IngestionResult(
                success=True,
                records_processed=len(all_records),
                quality_score=90.0,  # Base score for successful REST fetch
                lineage=lineage,
                raw_payload={
                    "records": all_records[:100]
                },  # Keep payload small for metadata
            )

        except Exception as e:
            logger.error(f"[{self.name}] REST fetch failed: {e}")
            lineage.extraction_duration_ms = int((time.time() - start_time) * 1000)
            return IngestionResult(
                success=False,
                quality_score=0.0,
                lineage=lineage,
                error_message=str(e),
            )

    async def fetch(self, *args: Any, **kwargs: Any) -> IngestionResult:
        return await self.fetch_paginated(*args, **kwargs)
