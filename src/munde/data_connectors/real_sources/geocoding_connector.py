"""
Tier 4 Connector: Geocoding and Reverse Geocoding.
Target: Translate coordinates to addresses and vice versa using OpenStreetMap Nominatim.
"""
import requests
import pandas as pd
from datetime import datetime
import structlog
from .base import BaseDataConnector

logger = structlog.get_logger(__name__)

class GeocodingConnector(BaseDataConnector):
    source_name = "OSM_Nominatim"
    
    def __init__(self, query_type: str = "reverse", lat: float = None, lon: float = None, address: str = None):
        self.query_type = query_type # 'reverse' or 'forward'
        self.lat = lat
        self.lon = lon
        self.address = address
        
    def fetch(self) -> pd.DataFrame:
        logger.info("fetching_geocoding_data", type=self.query_type)
        try:
            headers = {"User-Agent": "ProjectSahyadri/1.0 (contact: advait@example.com)"}
            
            if self.query_type == "reverse" and self.lat and self.lon:
                url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={self.lat}&lon={self.lon}"
            elif self.query_type == "forward" and self.address:
                url = f"https://nominatim.openstreetmap.org/search?format=json&q={self.address}&limit=1"
            else:
                return pd.DataFrame()
                
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if self.query_type == "reverse":
                addr = data.get("address", {})
                return pd.DataFrame([{
                    "latitude": self.lat, "longitude": self.lon,
                    "city": addr.get("city") or addr.get("town") or addr.get("village", "Unknown"),
                    "state": addr.get("state", "Maharashtra"),
                    "postcode": addr.get("postcode", "Unknown")
                }])
            else:
                if not data: return pd.DataFrame()
                return pd.DataFrame([{
                    "address_query": self.address,
                    "latitude": float(data[0].get("lat", 0.0)),
                    "longitude": float(data[0].get("lon", 0.0)),
                    "display_name": data[0].get("display_name", "Unknown")
                }])
                
        except requests.exceptions.RequestException as e:
            logger.error("geocoding_fetch_failed", error=str(e))
            return pd.DataFrame()
            
    def normalize(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        if raw_df.empty: return raw_df
        df = raw_df.copy()
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        df["source_url"] = "https://nominatim.openstreetmap.org/"
        df["is_live_telemetry"] = True
        return df
        
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        if df.empty: return df, 0.0
        score = 100.0 if not df.isnull().any().any() else 80.0
        return df, score
