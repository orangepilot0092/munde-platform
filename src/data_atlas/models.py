from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DatasetMetadata(BaseModel):
    """Standard metadata specification for Project Sahyadri."""

    dataset_id: str = Field(..., description="Unique identifier for the dataset")
    name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Detailed description")
    domain: str = Field(..., description="e.g., Agriculture, Water, Transport")
    department: str = Field(..., description="Publishing government department")
    source_url: str = Field(..., description="Official URL of the source")
    license: str = Field(default="Unknown", description="Data license type")
    format: str = Field(..., description="e.g., CSV, JSON, GeoJSON")
    refresh_frequency: str = Field(
        default="Manual", description="e.g., Daily, Weekly, Monthly"
    )
    last_updated: Optional[datetime] = None
    quality_score: Optional[float] = Field(
        None, ge=0, le=5, description="Quality score from 1-5"
    )
    tags: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "dataset_id": "ogd_maha_agri_001",
                "name": "Maharashtra Crop Production Statistics",
                "domain": "Agriculture",
                "department": "Department of Agriculture",
            }
        }
