from pydantic import BaseModel, UUID4, Field
from datetime import datetime

class AssetBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = None
    owner_department: str = Field(..., max_length=100)
    domain: str = Field(..., max_length=50)
    source_url: str | None = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: UUID4
    quality_score: float
    is_verified: bool
    version: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
