"""
Download Connector Protocol.
Handles direct file downloads with enterprise-grade redirect following and bot-protection bypass.
"""

import logging
import os
import tempfile
from typing import Any, Optional

import httpx
from src.core.connectors.base import BaseConnector, IngestionResult, LineageMetadata

logger = logging.getLogger(__name__)


class DownloadConnector(BaseConnector):
    def __init__(
        self,
        name: str,
        url: str,
        version: str = "1.0.0",
        timeout: float = 120.0,
        max_retries: int = 3,
        destination_dir: Optional[str] = None,
    ):
        super().__init__(
            name=name, version=version, timeout=timeout, max_retries=max_retries
        )
        self.url = url
        self.destination_dir = destination_dir or tempfile.gettempdir()

    async def fetch(self, *args: Any, **kwargs: Any) -> IngestionResult:
        import time

        start_time = time.time()
        lineage = LineageMetadata(
            source_system=self.name, source_url=self.url, connector_version=self.version
        )

        try:
            filename = self.url.split("/")[-1].split("?")[0] or "downloaded_file"
            filepath = os.path.join(self.destination_dir, filename)

            headers = {
                "User-Agent": "Sahyadri-Platform/1.0 (Open Data Ingestion; contact: admin@sahyadri.gov.in)"
            }

            async with httpx.AsyncClient(
                timeout=self.timeout, follow_redirects=True
            ) as client:
                async with client.stream("GET", self.url, headers=headers) as response:
                    response.raise_for_status()
                    file_size = 0
                    with open(filepath, "wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=8192):
                            f.write(chunk)
                            file_size += len(chunk)

            lineage.extraction_duration_ms = int((time.time() - start_time) * 1000)
            return IngestionResult(
                success=True,
                records_processed=1,
                quality_score=95.0,
                lineage=lineage,
                raw_payload={"file_path": filepath, "file_size_bytes": file_size},
            )
        except Exception as e:
            return IngestionResult(
                success=False, quality_score=0.0, lineage=lineage, error_message=str(e)
            )
