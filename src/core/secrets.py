import os
from typing import Optional
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class SecretsManager:
    API_KEY_MAP = {
        "api_imd_weather": "IMD_API_KEY",
        "api_data_gov_in": "DATA_GOV_IN_API_KEY",
        "api_bhuvan_wms": "BHUVAN_WMS_KEY",
        "api_msamb_apmc": "MSAMB_API_KEY",
        "api_mahabhulekh": "MAHABHULEKH_OAUTH_TOKEN",
        "api_mpcb_aqi": "MPCB_API_KEY",
        "api_wrd_reservoirs": "WRD_API_KEY",
    }

    @classmethod
    def get_api_key(cls, api_id: str) -> Optional[str]:
        env_var = cls.API_KEY_MAP.get(api_id)
        if not env_var:
            logger.warning(f"No env var mapping found for API: {api_id}")
            return None
        key = os.getenv(env_var)
        if key:
            logger.debug(f"API key loaded for {api_id} (length: {len(key)})")
            return key
        logger.info(
            f"API key not configured for {api_id} ({env_var}). Running in dry-run mode."
        )
        return None

    @classmethod
    def is_configured(cls, api_id: str) -> bool:
        return cls.get_api_key(api_id) is not None

    @classmethod
    def get_missing_apis(cls) -> list[str]:
        return [api_id for api_id in cls.API_KEY_MAP if not cls.is_configured(api_id)]
