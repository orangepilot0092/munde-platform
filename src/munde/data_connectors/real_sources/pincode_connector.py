"""
Tier 4 Connector: India PIN Code Lookup.
Target: Translate PIN codes to District, Taluka, and Post Office details.
"""
import requests
import pandas as pd
from datetime import datetime
import structlog
from .base import BaseDataConnector

logger = structlog.get_logger(__name__)

class PincodeConnector(BaseDataConnector):
    source_name = "India_Post_PIN"
    
    def __init__(self, pincode: str):
        self.pincode = pincode
        
    def fetch(self) -> pd.DataFrame:
        logger.info("fetching_pincode_data", pincode=self.pincode)
        try:
            # Official India Post PIN code API
            url = f"https://api.postalpincode.in/pincode/{self.pincode}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data[0].get("Status") == "Success":
                records = []
                for office in data[0].get("PostOffice", []):
                    records.append({
                        "pincode": self.pincode,
                        "post_office": office.get("Name", "Unknown"),
                        "district": office.get("District", "Unknown"),
                        "state": office.get("State", "Unknown"),
                        "delivery_status": office.get("DeliveryStatus", "Unknown")
                    })
                return pd.DataFrame(records)
            return pd.DataFrame()
            
        except requests.exceptions.RequestException as e:
            logger.error("pincode_fetch_failed", error=str(e))
            return pd.DataFrame()
            
    def normalize(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        if raw_df.empty: return raw_df
        df = raw_df.copy()
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        df["source_url"] = "https://api.postalpincode.in/"
        df["is_live_telemetry"] = False
        return df
        
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        if df.empty: return df, 0.0
        required = ["pincode", "post_office", "district", "state"]
        existing_req = [f for f in required if f in df.columns]
        score = round(sum(1 for f in existing_req if df[f].notna().all()) / len(existing_req) * 100, 2) if existing_req else 0.0
        return df.dropna(subset=["pincode", "district"]), score
