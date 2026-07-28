"""
Tier 1 Connector: Real-time Air Quality via WAQI API (Aggregates CPCB Data).
Target: Real-time AQI, PM2.5, and PM10 for major Maharashtra cities.
NO FALLBACK: Returns empty DataFrame if API fails.
"""
import requests
import pandas as pd
from datetime import datetime
import structlog
from .base import BaseDataConnector

logger = structlog.get_logger(__name__)

class CPCBConnector(BaseDataConnector):
    source_name = "WAQI_Air_Quality"
    
    def fetch(self) -> pd.DataFrame:
        logger.info("fetching_real_waqi_aqi_data")
        cities = ["mumbai", "pune", "nagpur", "nashik", "aurangabad", "kolhapur"]
        records = []
        
        try:
            for city in cities:
                # Using WAQI's public demo token (replace with your free token for production)
                url = f"https://api.waqi.info/feed/{city}/?token=demo"
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "ok" and "data" in data:
                    d = data["data"]
                    records.append({
                        "city": city.title(),
                        "aqi": d.get("aqi", 0),
                        "pm25": d.get("iaqi", {}).get("pm25", {}).get("v", 0),
                        "pm10": d.get("iaqi", {}).get("pm10", {}).get("v", 0),
                        "status": "Good" if d.get("aqi", 0) <= 50 else "Moderate" if d.get("aqi", 0) <= 100 else "Unhealthy"
                    })
            return pd.DataFrame(records)
        except requests.exceptions.RequestException as e:
            logger.error("waqi_api_failed_no_fallback", error=str(e))
            return pd.DataFrame() # STRICT: No fallback data
            
    def normalize(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        if raw_df.empty: return raw_df
        df = raw_df.copy()
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        df["source_url"] = "https://waqi.info/"
        df["is_live_telemetry"] = True
        return df
        
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        if df.empty: return df, 0.0
        required = ["city", "aqi", "pm25", "pm10", "status"]
        score = round(sum(1 for f in required if f in df.columns and df[f].notna().all()) / len(required) * 100, 2)
        return df.dropna(subset=["city", "aqi"]), score
