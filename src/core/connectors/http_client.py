import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class HttpClient:
    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException),
    )
    def get(url: str, params: dict = None):
        logger.info(f"Fetching {url}")
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
