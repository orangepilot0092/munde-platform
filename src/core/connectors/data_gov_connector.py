"""
Data.gov.in OData REST API Connector
Verified: 2026-07-09
Key Finding: Use LG_ST_Code (numeric) for state filtering, NOT State (string).
             Maharashtra = LG_ST_Code 27. State names are UPPERCASE.
"""

from typing import Any, Optional
import requests
from src.core.connectors.live_base import LiveConnectorBase
from src.core.logging_config import get_logger

logger = get_logger(__name__)

# Verified Maharashtra LGD State Code
MH_LG_ST_CODE = "27"


class DataGovInConnector(LiveConnectorBase):
    def __init__(self):
        super().__init__("api_data_gov_in", "Data.gov.in OData (Maharashtra)")
        self.base_url = "https://api.data.gov.in/resource"

    def fetch_live(
        self,
        resource_id: str = "8b68ae56-84cf-4728-a0a6-1be11028dea7",
        limit: int = 100,
        filters: Optional[dict] = None,
        **kwargs,
    ) -> Any:
        params = {
            "api-key": self.api_key,
            "format": "json",
            "limit": limit,
        }
        # Always default to Maharashtra via LG_ST_Code unless overridden
        if filters is None:
            filters = {}
        if "LG_ST_Code" not in filters and "State" not in filters:
            filters["LG_ST_Code"] = MH_LG_ST_CODE

        for k, v in filters.items():
            params[f"filters[{k}]"] = v

        logger.info(
            f"Fetching Data.gov.in resource {resource_id} with filters: {filters}"
        )
        resp = requests.get(f"{self.base_url}/{resource_id}", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_sample_data(self, **kwargs) -> Any:
        return {
            "records": [
                {
                    "State": "MAHARASHTRA",
                    "District": "Pune",
                    "EnterpriseName": "Sample MSME Unit",
                    "LG_ST_Code": "27",
                    "RegistrationDate": "2024-06-15",
                },
                {
                    "State": "MAHARASHTRA",
                    "District": "Nashik",
                    "EnterpriseName": "Sample Agro Industry",
                    "LG_ST_Code": "27",
                    "RegistrationDate": "2024-07-01",
                },
            ],
            "total": 2,
            "note": "SAMPLE DATA — Configure DATA_GOV_IN_API_KEY for live data. Use LG_ST_Code=27 for Maharashtra.",
        }
