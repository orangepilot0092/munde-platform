"""
Tier 1 Connector: Real-time Weather Data via Open-Meteo (IMD Proxy).
NO FALLBACK: Returns empty DataFrame if API fails.
"""
import requests
import pandas as pd
from datetime import datetime
import structlog
from .base import BaseDataConnector

logger = structlog.get_logger(__name__)

class IMDConnector(BaseDataConnector):
    source_name = "IMD_Weather"
    
    def fetch(self) -> pd.DataFrame:
        logger.info("fetching_real_imd_weather_data")
        locations = {"Pune": (18.52, 73.85), "Nashik": (19.99, 73.78), "Nagpur": (21.14, 79.08), "Mumbai": (19.07, 72.87), "Aurangabad": (19.87, 75.34), "Kolhapur": (16.70, 74.24)}
        records = []
        try:
            for district, (lat, lon) in locations.items():
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,rain,weather_code"
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()["current"]
                code = data.get("weather_code", 0)
                condition = "Rain" if code > 50 else "Cloudy" if code > 3 else "Clear"
                records.append({"district": district, "temperature_c": data.get("temperature_2m", 0.0), "rainfall_mm": data.get("rain", 0.0), "condition": condition})
            return pd.DataFrame(records)
        except requests.exceptions.RequestException as e:
            logger.error("imd_api_failed_no_fallback", error=str(e))
            return pd.DataFrame() # STRICT: No fallback data
            
    def normalize(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        if raw_df.empty: return raw_df
        df = raw_df.copy()
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        df["source_url"] = "https://open-meteo.com/"
        df["is_live_telemetry"] = True
        return df
        
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        if df.empty: return df, 0.0
        required = ["district", "temperature_c", "rainfall_mm", "date"]
        score = round(sum(1 for f in required if f in df.columns and df[f].notna().all()) / len(required) * 100, 2)
        return df.dropna(subset=["district", "temperature_c"]), score
