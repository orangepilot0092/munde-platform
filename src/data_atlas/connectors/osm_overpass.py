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


class OSMAPIError(Exception):
    """Custom exception for OSM API failures."""

    pass


class OSMOverpassConnector:
    """
    Tier 1 Connector: OpenStreetMap Overpass API.
    Fetches geospatial data without authentication, with built-in retry logic.
    """

    def __init__(self, endpoint: str = "https://overpass-api.de/api/interpreter"):
        self.endpoint = endpoint
        self.timeout = 60.0

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=20),
        retry=retry_if_exception_type(
            (httpx.TimeoutException, httpx.HTTPStatusError, httpx.RequestError)
        ),
        reraise=True,
    )
    async def fetch_geospatial_data(self, query: str) -> Dict[str, Any]:  # type: ignore[misc]
        logger.info(f"Executing OSM Overpass query (length: {len(query)} chars)")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    self.endpoint,
                    data={"data": query},
                    headers={
                        "User-Agent": "ProjectSahyadri/1.0 (https://sahyadri.ai; advait@sahyadri.ai)"
                    },
                )
                response.raise_for_status()
                logger.info("✅ Successfully fetched data from OSM Overpass API")
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException:
                logger.warning("⚠️ OSM Overpass API timed out. Retrying...")
                raise
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"❌ OSM Overpass API returned HTTP {e.response.status_code}"
                )
                raise OSMAPIError(f"HTTP Error: {e.response.status_code}") from e
            except httpx.RequestError as e:
                logger.error(f"❌ Network error connecting to OSM Overpass: {e}")
                raise

    async def get_maharashtra_district_boundaries(
        self, district_name: str
    ) -> Dict[str, Any]:
        # Direct query for district boundary without area constraint
        query = f"""
        [out:json][timeout:60];
        relation["name"="{district_name}"]["admin_level"~"^[56]$"]["boundary"="administrative"];
        out body;
        >;
        out skel qt;
        """
        return await self.fetch_geospatial_data(query)
