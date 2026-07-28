"""
Base Connector Interface for Project Sahyadri.
Ensures all data sources follow the fetch -> normalize -> validate -> ingest pattern.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import pandas as pd

class BaseDataConnector(ABC):
    source_name: str = "BaseSource"
    
    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        """Fetch raw data from the source (API, CSV, WMS, etc.)"""
        pass
    
    @abstractmethod
    def normalize(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """Clean, rename columns, and standardize the data."""
        pass
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
        """Check for nulls, duplicates, and return (clean_df, quality_score)."""
        pass
    
    def ingest(self, df: pd.DataFrame, quality_score: float) -> Dict[str, Any]:
        """Placeholder for ingestion logic (handled by Dagster assets)."""
        return {"records_processed": len(df), "quality_score": quality_score, "status": "success"}
