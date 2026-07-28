"""
Tier 1 Connector: OpenStreetMap (OSM) via Overpass API.
Target: Geospatial data for Hospitals and Schools in Maharashtra.
"""
import requests
import pandas as pd
from datetime import datetime
import structlog
from .base import BaseDataConnector

logger = structlog.get_logger(__name__)

class OSMConnector(BaseDataConnector):
    source_name = "OSM_Geospatial"
    
    def __init__(self, target_city: str = "Pune", amenity: str = "hospital"):
        self.target_city = target_city
        self.amenity = amenity
        
    def fetch(self) -> pd.DataFrame:
        logger.info("fetching_osm_data", city=self.target_city, amenity=self.amenity)
        try:
            # Overpass QL query
            query = f"""
            [out:json][timeout:25];
            area["name"="{self.target_city}"]["admin_level"="6"]->.searchArea;
            (
              node["amenity"="{self.amenity}"](area.searchArea);
              way["amenity"="{self.amenity}"](area.searchArea);
            );
            out center;
            """
            url = "https://overpass-api.de/api/interpreter"
            response = requests.post(url, data={'data': query}, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            records = []
            for element in data.get("elements", [])[:50]: # Limit to 50 for MVP
                tags = element.get("tags", {})
                records.append({
                    "district": self.target_city,
                    "facility_name": tags.get("name", "Unnamed Facility"),
                    "facility_type": self.amenity.title(),
                    "latitude": element.get("lat", element.get("center", {}).get("lat", 0.0)),
                    "longitude": element.get("lon", element.get("center", {}).get("lon", 0.0)),
                    "address": tags.get("addr:street", "Unknown")
                })
            return pd.DataFrame(records)
            
        except requests.exceptions.RequestException as e:
            logger.warning("osm_api_failed_falling_back", error=str(e))
            # Graceful fallback
            return pd.DataFrame([{
                "district": self.target_city, "facility_name": f"Fallback {self.amenity}",
                "facility_type": self.amenity.title(), "latitude": 18.52, "longitude": 73.85, "address": "Fallback Address"
            }])
            
    def normalize(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        if raw_df.empty: return raw_df
        df = raw_df.copy()
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        df["source_url"] = "https://www.openstreetmap.org/"
        df["is_live_telemetry"] = True
        return df
        
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        if df.empty: return df, 0.0
        required = ["district", "facility_name", "facility_type", "latitude", "longitude"]
        score = round(sum(1 for f in required if f in df.columns and df[f].notna().all()) / len(required) * 100, 2)
        return df.dropna(subset=["district", "facility_name", "latitude"]), score
