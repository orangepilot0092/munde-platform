from typing import Any
import requests
from src.core.connectors.live_base import LiveConnectorBase


class MSAMBAPMCConnector(LiveConnectorBase):
    def __init__(self):
        super().__init__("api_msamb_apmc", "MSAMB APMC Market Prices")
        self.base_url = "https://msamb.com/api/v1"

    def fetch_live(
        self, market: str = "Pune", commodity: str = "Sugarcane", **kwargs
    ) -> Any:
        resp = requests.get(
            f"{self.base_url}/arrivals",
            params={"market": market, "commodity": commodity},
            headers={"X-API-Key": self.api_key},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()

    def get_sample_data(self, market: str = "Pune", **kwargs) -> Any:
        return {
            "market": market,
            "date": "2026-07-08",
            "arrivals": [
                {
                    "commodity": "Sugarcane",
                    "arrival_qt": 4500,
                    "min_price": 2800,
                    "max_price": 3200,
                    "modal_price": 3050,
                },
                {
                    "commodity": "Cotton",
                    "arrival_qt": 1200,
                    "min_price": 5500,
                    "max_price": 6200,
                    "modal_price": 5900,
                },
            ],
            "note": "SAMPLE DATA - Configure MSAMB_API_KEY for live arrivals",
        }
