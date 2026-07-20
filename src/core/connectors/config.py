"""
Pydantic schemas for configuration-driven connector definitions.
"""

from typing import Annotated, Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

OperationalStatus = Literal["connected", "ready", "file_based", "blocked"]


class BaseConnectorConfig(BaseModel):
    name: str = Field(..., description="Unique identifier")
    description: Optional[str] = None
    domain: Optional[str] = None
    schedule: Optional[str] = None
    status: OperationalStatus = "connected"
    blocked_reason: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # New Operational Fields
    ssl_verify: bool = Field(True, description="Whether to verify SSL certificates")
    auth_required: bool = Field(
        False,
        description="Whether this source requires API keys/tokens not present in the repo",
    )


class RESTConnectorConfig(BaseConnectorConfig):
    type: Literal["rest"] = "rest"
    url: str
    method: Literal["GET", "POST"] = "GET"
    headers: Dict[str, str] = Field(default_factory=dict)
    params: Dict[str, Any] = Field(default_factory=dict)
    pagination_key: Optional[str] = None


class STACConnectorConfig(BaseConnectorConfig):
    type: Literal["stac"] = "stac"
    catalog_url: str
    collections: List[str]
    bbox: Optional[List[float]] = None
    datetime_range: Optional[str] = None
    limit: int = 50


class DownloadConnectorConfig(BaseConnectorConfig):
    type: Literal["download"] = "download"
    url: str
    destination_dir: Optional[str] = None


class ScraperConnectorConfig(BaseConnectorConfig):
    type: Literal["scraper"] = "scraper"
    url: str


class ManualConnectorConfig(BaseConnectorConfig):
    type: Literal["manual"] = "manual"
    url: str


ConnectorConfig = Annotated[
    Union[
        RESTConnectorConfig,
        STACConnectorConfig,
        DownloadConnectorConfig,
        ScraperConnectorConfig,
        ManualConnectorConfig,
    ],
    Field(discriminator="type"),
]
