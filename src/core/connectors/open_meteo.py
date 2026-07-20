"""
Open-Meteo Weather Forecast Connector
Verified: 2026-07-09 against https://open-meteo.com/en/docs/weather-api
Source: https://api.open-meteo.com/v1/forecast
Domain: Weather / Water / Agriculture
Access: No API key required (non-commercial, <10K daily calls)
"""

from typing import Any
import requests
from pydantic import BaseModel
from src.core.connectors.live_base import LiveConnectorBase
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class DailyForecast(BaseModel):
    time: list[str]
    temperature_2m_max: list[float]
    temperature_2m_min: list[float]
    precipitation_sum: list[float]
    rain_sum: list[float]
    showers_sum: list[float]
    snowfall_sum: list[float]
    weather_code: list[int]
    sunrise: list[str]
    sunset: list[str]


class DailyUnits(BaseModel):
    time: str = "iso8601"
    temperature_2m_max: str = "°C"
    temperature_2m_min: str = "°C"
    precipitation_sum: str = "mm"
    rain_sum: str = "mm"
    showers_sum: str = "mm"
    snowfall_sum: str = "cm"
    weather_code: str = "wmo code"
    sunrise: str = "iso8601"
    sunset: str = "iso8601"


class OpenMeteoResponse(BaseModel):
    latitude: float
    longitude: float
    elevation: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    daily: DailyForecast
    daily_units: DailyUnits


class OpenMeteoConnector(LiveConnectorBase):
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    DEFAULT_LAT = 18.5204
    DEFAULT_LON = 73.8567
    DAILY_PARAMS = "temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,showers_sum,snowfall_sum,weather_code,sunrise,sunset"

    def __init__(self):
        super().__init__("open_meteo_pune", "Open-Meteo Weather Forecast")
        self.is_live = True  # No API key required
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "ProjectSahyadri/1.0 (DPI Research Bot; contact@sahyadri.ai)",
                "Accept": "application/json",
            }
        )

    def fetch_live(
        self,
        latitude: float = DEFAULT_LAT,
        longitude: float = DEFAULT_LON,
        forecast_days: int = 7,
        **kwargs,
    ) -> Any:
        """Return RAW validated data. Base class wraps in {status, source, data}."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": self.DAILY_PARAMS,
            "timezone": "Asia/Kolkata",
            "forecast_days": min(max(forecast_days, 1), 16),
        }
        logger.info(
            f"Fetching Open-Meteo forecast: lat={latitude}, lon={longitude}, days={params['forecast_days']}"
        )
        resp = self.session.get(self.BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        validated = OpenMeteoResponse(**resp.json())
        logger.info(
            f"Open-Meteo returned {len(validated.daily.time)} days for {validated.timezone}"
        )
        return validated.model_dump()  # Raw data only; base class handles wrapping

    def get_sample_data(self, **kwargs) -> Any:
        """Return RAW sample data. Base class wraps in {status, source, data}."""
        sample = OpenMeteoResponse(
            latitude=18.5204,
            longitude=73.8567,
            elevation=542.0,
            generationtime_ms=0.13,
            utc_offset_seconds=19800,
            timezone="Asia/Kolkata",
            timezone_abbreviation="GMT+5:30",
            daily=DailyForecast(
                time=["2026-07-09", "2026-07-10", "2026-07-11"],
                temperature_2m_max=[28.4, 28.7, 28.8],
                temperature_2m_min=[22.1, 22.3, 22.5],
                precipitation_sum=[0.5, 0.0, 0.2],
                rain_sum=[0.5, 0.0, 0.2],
                showers_sum=[0.0, 0.0, 0.0],
                snowfall_sum=[0.0, 0.0, 0.0],
                weather_code=[61, 0, 51],
                sunrise=["2026-07-09T06:02", "2026-07-10T06:02", "2026-07-11T06:03"],
                sunset=["2026-07-09T19:15", "2026-07-10T19:15", "2026-07-11T19:15"],
            ),
            daily_units=DailyUnits(),
        )
        return sample.model_dump()
