"""
Live Connector Base Class with Circuit Breaker
Sprint 34 — Production resilience for government APIs
Per 02_ARCHITECTURE_AND_INFRA.md Layer 2: Retry logic + circuit breaker pattern
"""

from abc import ABC, abstractmethod
from typing import Any
from circuitbreaker import circuit
from src.core.secrets import SecretsManager
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class LiveConnectorBase(ABC):
    def __init__(self, api_id: str, name: str):
        self.api_id = api_id
        self.name = name
        self.api_key = SecretsManager.get_api_key(api_id)
        self.is_live = self.api_key is not None

    @abstractmethod
    def fetch_live(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def get_sample_data(self, **kwargs) -> Any:
        pass

    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    def fetch(self, **kwargs) -> dict:
        """Fetch with circuit breaker: opens after 5 failures, recovers after 60s."""
        if self.is_live:
            logger.info(f"[LIVE] Fetching from {self.name}")
            try:
                data = self.fetch_live(**kwargs)
                return {"status": "live", "source": self.name, "data": data}
            except Exception as e:
                logger.error(f"[LIVE] API call failed for {self.name}: {e}")
                return {"status": "error", "source": self.name, "error": str(e)}
        else:
            logger.info(f"[DRY-RUN] Using sample data for {self.name} (no API key)")
            data = self.get_sample_data(**kwargs)
            return {"status": "dry_run", "source": self.name, "data": data}
