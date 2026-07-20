"""
OSM Overpass API Connector
Verified: 2026-07-09 against https://wiki.openstreetmap.org/wiki/Overpass_API
Note: Overpass API requires explicit Content-Type header for POST requests.
      Maharashtra-wide queries can take 30-60s; client timeout must exceed server timeout.
"""

from typing import Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.core.connectors.live_base import LiveConnectorBase
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class OSMOverpassConnector(LiveConnectorBase):
    BASE_URL = "https://overpass-api.de/api/interpreter"

    QUERY_TEMPLATES = {
        "hospitals": '[out:json][timeout:60];area["name"="Maharashtra"]->.mh;node(area.mh)["amenity"="hospital"];out body;',
        "schools": '[out:json][timeout:60];area["name"="Maharashtra"]->.mh;node(area.mh)["amenity"="school"];out body;',
        "water_bodies": '[out:json][timeout:60];area["name"="Maharashtra"]->.mh;way(area.mh)["natural"="water"];out body;',
        "roads": '[out:json][timeout:60];area["name"="Maharashtra"]->.mh;way(area.mh)["highway"~"primary|secondary|tertiary"];out body;',
    }

    def __init__(self):
        # api_id must match SecretsManager key; name is display name
        super().__init__("osm_overpass", "OSM Overpass (Maharashtra)")
        # OSM needs no API key but we force is_live=True since base class sets False when no key
        self.is_live = True
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "ProjectSahyadri/1.0 (DPI Research Bot; contact@sahyadri.ai)",
                "Accept": "application/json",
            }
        )
        retries = Retry(total=3, backoff_factor=5, status_forcelist=[502, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def fetch_live(
        self,
        query_type: str = "hospitals",
        custom_query: Optional[str] = None,
        timeout: int = 90,
        **kwargs,
    ) -> Any:
        """Return RAW data only. Base class wraps in {status, source, data}."""
        query = custom_query or self.QUERY_TEMPLATES.get(query_type)
        if not query:
            raise ValueError(
                f"Unknown query_type '{query_type}'. Available: {list(self.QUERY_TEMPLATES.keys())}"
            )

        logger.info(f"Fetching OSM data: query_type={query_type}, timeout={timeout}s")
        resp = self.session.post(self.BASE_URL, data={"data": query}, timeout=timeout)
        resp.raise_for_status()
        result = resp.json()
        element_count = len(result.get("elements", []))
        logger.info(f"OSM returned {element_count} elements for {query_type}")
        return result  # Raw data only; base class handles wrapping

    def get_sample_data(self, **kwargs) -> Any:
        """Return RAW sample data. Base class wraps in {status, source, data}."""
        return {
            "version": 0.6,
            "generator": "Overpass API (Sample)",
            "elements": [
                {
                    "type": "node",
                    "id": 1,
                    "lat": 18.5204,
                    "lon": 73.8567,
                    "tags": {"amenity": "hospital", "name": "Sassoon General Hospital"},
                },
                {
                    "type": "node",
                    "id": 2,
                    "lat": 18.5293,
                    "lon": 73.8432,
                    "tags": {
                        "amenity": "hospital",
                        "name": "Deenanath Mangeshkar Hospital",
                    },
                },
            ],
        }
