"""
Standardized Base Connector for Project Sahyadri.
Enforces timeouts, retries, typing, and lineage tracking for all data ingestion.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import httpx

logger = logging.getLogger(__name__)


class LineageMetadata(BaseModel):
    """Standardized lineage metadata for every ingestion run."""

    source_system: str
    source_url: Optional[str] = None
    connector_version: str
    extraction_timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    extraction_duration_ms: Optional[int] = None
    record_count: int = 0
    filters_applied: Dict[str, Any] = Field(default_factory=dict)


class IngestionResult(BaseModel):
    """Standardized result returned by all connectors."""

    success: bool
    records_processed: int = 0
    records_failed: int = 0
    quality_score: float = Field(ge=0.0, le=100.0, default=0.0)
    lineage: LineageMetadata
    error_message: Optional[str] = None
    raw_payload: Optional[Dict[str, Any]] = None  # For debugging/audit, keep small


class BaseConnector(ABC):
    """
    Abstract base class for all Sahyadri data connectors.
    Enforces retry logic, timeouts, and standardized output.
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.name = name
        self.version = version
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                headers={
                    "User-Agent": "ProjectSahyadri/1.0 (https://sahyadri.ai; sovereign-ai@maharashtra.gov.in)",
                    "Accept": "application/json",
                },
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client connection."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @retry(  # type: ignore[misc]
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=20),
        retry=retry_if_exception_type(
            (httpx.TimeoutException, httpx.HTTPStatusError, httpx.RequestError)
        ),
        reraise=True,
    )
    async def _request_with_retry(
        self, method: str, url: str, **kwargs: Any
    ) -> httpx.Response:
        """Internal method to handle resilient HTTP requests."""
        logger.debug(f"[{self.name}] Requesting {method} {url}")
        response = await self.client.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    @abstractmethod
    async def fetch(self, *args: Any, **kwargs: Any) -> IngestionResult:
        """
        Core ingestion logic. Must be implemented by subclasses.
        Must return an IngestionResult with standardized lineage.
        """
        pass
