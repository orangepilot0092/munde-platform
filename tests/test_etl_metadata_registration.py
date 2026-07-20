"""
Integration tests for the Metadata Registration Dagster pipeline.
"""

from dagster import AssetsDefinition

from etl.sahyadri_etl.assets.metadata_registration import (
    register_weather_open_meteo_metadata,
)


def test_metadata_registration_asset_is_valid() -> None:
    """Test that the asset is correctly defined as a Dagster AssetsDefinition."""
    assert isinstance(register_weather_open_meteo_metadata, AssetsDefinition)

    # Verify the asset key matches our expected name
    asset_keys = [
        key.to_python_identifier() for key in register_weather_open_meteo_metadata.keys
    ]
    assert "register_weather_open_meteo_metadata" in asset_keys
    assert len(register_weather_open_meteo_metadata.keys) > 0


def test_metadata_registration_has_correct_dependencies() -> None:
    """Test that the metadata registration asset depends on the weather ingestion asset."""
    input_keys = register_weather_open_meteo_metadata.keys_by_input_name
    dep_names = [key.to_python_identifier() for key in input_keys.values()]

    assert "weather_open_meteo_maharashtra" in dep_names
