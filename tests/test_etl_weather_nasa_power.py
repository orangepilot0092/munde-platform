"""
Integration tests for the NASA POWER Dagster ETL pipeline.
"""

from dagster import AssetsDefinition

from etl.sahyadri_etl.assets.weather_nasa_power import weather_nasa_power_maharashtra
from etl.sahyadri_etl.assets.metadata_registry_update import (
    metadata_registry_weather_nasa_power,
)


def test_weather_nasa_power_asset_is_valid() -> None:
    """Test that the asset is correctly defined as a Dagster AssetsDefinition."""
    assert isinstance(weather_nasa_power_maharashtra, AssetsDefinition)

    # Verify the asset key matches our expected name
    asset_keys = [
        key.to_python_identifier() for key in weather_nasa_power_maharashtra.keys
    ]
    assert "weather_nasa_power_maharashtra" in asset_keys


def test_metadata_registry_asset_dependencies() -> None:
    """Test that the metadata update asset correctly depends on the ingestion asset."""
    assert isinstance(metadata_registry_weather_nasa_power, AssetsDefinition)

    # Verify the dependency is correctly wired via input keys
    input_keys = metadata_registry_weather_nasa_power.keys_by_input_name
    dep_keys = [key.to_python_identifier() for key in input_keys.values()]

    assert "weather_nasa_power_maharashtra" in dep_keys
