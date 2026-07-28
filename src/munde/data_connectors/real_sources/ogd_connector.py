"""
Tier 1 Connector: India Open Government Data (OGD) Platform.
Target: Agmarknet Daily Market Prices for Maharashtra.
NO FALLBACK: Returns empty DataFrame if API fails.
"""
import requests
import pandas as pd
from datetime import datetime
import structlog
from .base import BaseDataConnector

logger = structlog.get_logger(__name__)

class OGDConnector(BaseDataConnector):
    source_name = "India_OGD_Agmarknet"
    
    def __init__(self, api_key: str, resource_id: str = "9ef94c48-1898-4d5c-bd85-68a5c0b8a4e8"):
        self.api_key = api_key
        self.resource_id = resource_id
        self.base_url = "https://api.data.gov.in/resource/"
        
    def fetch(self) -> pd.DataFrame:
        logger.info("fetching_real_ogd_data", resource_id=self.resource_id)
        params = {"api-key": self.api_key, "format": "json", "limit": 500}
        try:
            response = requests.get(f"{self.base_url}{self.resource_id}", params=params, timeout=30)
            response.raise_for_status()
            raw_df = pd.DataFrame(response.json().get("records", []))
            if not raw_df.empty and 'state' in raw_df.columns:
                return raw_df[raw_df['state'].str.contains('Maharashtra', case=False, na=False)]
            return raw_df
        except requests.exceptions.RequestException as e:
            logger.error("ogd_api_failed_no_fallback", error=str(e))
            return pd.DataFrame() # STRICT: No fallback data
            
    def normalize(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        if raw_df.empty: return raw_df
        df = raw_df.rename(columns={"district": "district", "market": "taluka", "commodity": "crop", "modal_price": "market_price_per_quintal"})
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        df["source_url"] = "https://data.gov.in/"
        df["is_live_telemetry"] = True
        return df
        
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        if df.empty: return df, 0.0
        required = ["district", "taluka", "crop", "market_price_per_quintal", "date"]
        score = round(sum(1 for f in required if f in df.columns and df[f].notna().all()) / len(required) * 100, 2)
        return df.dropna(subset=["district", "crop", "market_price_per_quintal"]), score
