from typing import Any
import requests
from src.core.connectors.live_base import LiveConnectorBase


class IMDWeatherConnector(LiveConnectorBase):
    def __init__(self):
        super().__init__("api_imd_weather", "IMD Pune Weather Forecast")
        self.base_url = "https://mausam.imd.gov.in/api"

    def fetch_live(self, district: str = "Pune", **kwargs) -> Any:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.get(
            f"{self.base_url}/forecast/district",
            params={"district": district},
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()

    def get_sample_data(self, district: str = "Pune", **kwargs) -> Any:
        return {
            "district": district,
            "forecast": [
                {
                    "date": "2026-07-09",
                    "max_temp": 32,
                    "min_temp": 24,
                    "rainfall_mm": 5.2,
                },
                {
                    "date": "2026-07-10",
                    "max_temp": 30,
                    "min_temp": 23,
                    "rainfall_mm": 12.8,
                },
                {
                    "date": "2026-07-11",
                    "max_temp": 29,
                    "min_temp": 22,
                    "rainfall_mm": 18.5,
                },
            ],
            "note": "SAMPLE DATA - Configure IMD_API_KEY for live data",
        }
