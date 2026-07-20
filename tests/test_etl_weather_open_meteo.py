"""
Integration tests for the Open-Meteo Dagster ETL pipeline.
"""

from dagster import AssetsDefinition

from etl.sahyadri_etl.assets.weather_open_meteo import weather_open_meteo_maharashtra


def test_weather_open_meteo_asset_is_valid() -> None:
    """Test that the asset is correctly defined as a Dagster AssetsDefinition."""
    assert isinstance(weather_open_meteo_maharashtra, AssetsDefinition)

    # Verify the asset key matches our expected name
    asset_keys = [
        key.to_python_identifier() for key in weather_open_meteo_maharashtra.keys
    ]
    assert "weather_open_meteo_maharashtra" in asset_keys
    assert len(weather_open_meteo_maharashtra.keys) > 0
