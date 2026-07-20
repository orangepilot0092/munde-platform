"""
Tier 1 Connector: NASA POWER API.
Fetches meteorological data without authentication.
Refactored to inherit from BaseConnector for standardized lineage and retries.
"""

import logging
import time
from typing import Any, List, Optional

from src.core.connectors.base import BaseConnector, IngestionResult, LineageMetadata

logger = logging.getLogger(__name__)

DEFAULT_PARAMETERS = ["PRECTOTCORR", "T2M_MAX", "T2M_MIN"]


class NASAPowerConnector(BaseConnector):
    """
    Connector for NASA POWER meteorological data.
    Tier 1: No authentication required.
    """

    def __init__(
        self,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        super().__init__(
            name="nasa_power",
            version="1.0.0",
            timeout=timeout,
            max_retries=max_retries,
        )
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    async def fetch_daily_point_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,  # YYYYMMDD
        end_date: str,  # YYYYMMDD
        parameters: Optional[List[str]] = None,
    ) -> IngestionResult:
        """
        Fetch daily point data for a single coordinate.
        Returns a standardized IngestionResult with lineage metadata.
        """
        params = parameters or DEFAULT_PARAMETERS
        start_time = time.time()

        lineage = LineageMetadata(
            source_system="NASA POWER API",
            source_url=self.base_url,
            connector_version=self.version,
            filters_applied={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "parameters": params,
            },
        )

        try:
            query_params = {
                "parameters": ",".join(params),
                "community": "AG",  # Agriculture community
                "longitude": longitude,
                "latitude": latitude,
                "start": start_date,
                "end": end_date,
                "format": "JSON",
            }

            response = await self._request_with_retry(
                "GET", self.base_url, params=query_params
            )
            data = response.json()

            # Count records across all parameters to estimate volume
            param_data = data.get("properties", {}).get("parameter", {})
            record_count = 0
            for param_values in param_data.values():
                if isinstance(param_values, dict):
                    record_count = max(record_count, len(param_values))

            duration_ms = int((time.time() - start_time) * 1000)
            lineage.extraction_duration_ms = duration_ms
            lineage.record_count = record_count

            return IngestionResult(
                success=True,
                records_processed=record_count,
                quality_score=92.0,  # NASA POWER is highly reliable
                lineage=lineage,
                raw_payload=data,
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            lineage.extraction_duration_ms = duration_ms
            logger.error(
                f"[nasa_power] Fetch failed for lat:{latitude}, lon:{longitude}: {e}"
            )
            return IngestionResult(
                success=False,
                quality_score=0.0,
                lineage=lineage,
                error_message=str(e),
            )

    async def fetch(self, *args: Any, **kwargs: Any) -> IngestionResult:
        """
        Abstract method implementation. Delegates to fetch_daily_point_data.
        """
        return await self.fetch_daily_point_data(*args, **kwargs)
