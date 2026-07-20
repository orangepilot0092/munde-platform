"""
Tier 1 Connector: GBIF API (Global Biodiversity Information Facility).
Fetches open biodiversity and agricultural occurrence data without authentication.
"""

import httpx
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from typing import Dict, Any

logger = logging.getLogger(__name__)


class GBIFAPIError(Exception):
    """Custom exception for GBIF API failures."""

    pass


class GBIFConnector:
    def __init__(self, base_url: str = "https://api.gbif.org/v1"):
        self.base_url = base_url
        self.timeout = 30.0

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=20),
        retry=retry_if_exception_type(
            (httpx.TimeoutException, httpx.HTTPStatusError, httpx.RequestError)
        ),
        reraise=True,
    )
    async def search_occurrences(
        self, country: str = "IN", state_province: str = "Maharashtra", limit: int = 200
    ) -> Dict[str, Any]:
        """
        Search for species/crop occurrences in a specific region.
        """
        url = f"{self.base_url}/occurrence/search"
        params = {
            "country": country,
            "stateProvince": state_province,
            "hasCoordinate": "true",
            "limit": limit,
        }

        headers = {
            "User-Agent": "ProjectSahyadri/1.0 (https://sahyadri.ai; advait@sahyadri.ai)",
            "Accept": "application/json",
        }

        logger.info(
            f"Fetching GBIF occurrences for {state_province}, {country} (limit: {limit})..."
        )

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info(
                    f"✅ Successfully fetched {data.get('count', 0)} records from GBIF API"
                )
                return data
            except httpx.TimeoutException:
                logger.warning("⚠️ GBIF API timed out. Retrying...")
                raise
            except httpx.HTTPStatusError as e:
                logger.error(f"❌ GBIF API returned HTTP {e.response.status_code}")
                raise GBIFAPIError(f"HTTP Error: {e.response.status_code}") from e
            except httpx.RequestError as e:
                logger.error(f"❌ Network error connecting to GBIF: {e}")
                raise
