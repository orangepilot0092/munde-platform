from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class DatasetSummary(BaseModel):
    dataset_id: str
    name: str
    domain: Optional[str] = None
    quality_score: Optional[float] = None
    last_updated: Optional[datetime] = None
    tags: Optional[List[str]] = None
    # Multilingual fields
    name_mr: Optional[str] = None
    name_hi: Optional[str] = None


class DatasetDetail(DatasetSummary):
    description: Optional[str] = None
    description_mr: Optional[str] = None
    description_hi: Optional[str] = None
    department: Optional[str] = None
    source_url: Optional[str] = None
    license: Optional[str] = None
    format: Optional[str] = None
    refresh_frequency: Optional[str] = None
    storage_path: Optional[str] = None
    lineage: Optional[Dict[str, Any]] = None
    validation_report: Optional[Dict[str, Any]] = None
    freshness_score: Optional[float] = None
    completeness_score: Optional[float] = None
    machine_readability_score: Optional[float] = None


class AtlasStats(BaseModel):
    total_datasets: int
    domains_covered: List[str]
    average_quality_score: float
    atlas_version: str = "1.0.0"
