from typing import Any
import requests
from src.core.connectors.live_base import LiveConnectorBase


class BhuvanWMSConnector(LiveConnectorBase):
    def __init__(self):
        super().__init__("api_bhuvan_wms", "ISRO Bhuvan WMS")
        self.base_url = "https://bhuvan-app1.nrsc.gov.in/api/wms"

    def fetch_live(
        self, layer: str = "land_use", bbox: str = "73.8,18.4,74.0,18.6", **kwargs
    ) -> Any:
        resp = requests.get(
            self.base_url,
            params={
                "service": "WMS",
                "request": "GetMap",
                "layers": layer,
                "bbox": bbox,
                "width": 256,
                "height": 256,
                "format": "image/png",
                "api_key": self.api_key,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return {
            "content_type": resp.headers.get("content-type"),
            "size_bytes": len(resp.content),
        }

    def get_sample_data(self, **kwargs) -> Any:
        return {
            "layer": "land_use",
            "bbox": "73.8,18.4,74.0,18.6",
            "format": "image/png",
            "note": "SAMPLE DATA - Configure BHUVAN_WMS_KEY for live tiles",
        }
