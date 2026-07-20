"""
Integration tests for the EO STAC Dagster pipelines.
"""

from dagster import AssetsDefinition

from etl.sahyadri_etl.assets.eo_stac_sentinel2 import eo_stac_sentinel2_maharashtra
from etl.sahyadri_etl.assets.metadata_registration_eo import register_eo_stac_metadata


def test_eo_stac_asset_is_valid() -> None:
    """Test that the EO STAC asset is correctly defined."""
    assert isinstance(eo_stac_sentinel2_maharashtra, AssetsDefinition)
    asset_keys = [
        key.to_python_identifier() for key in eo_stac_sentinel2_maharashtra.keys
    ]
    assert "eo_stac_sentinel2_maharashtra" in asset_keys


def test_eo_metadata_registration_asset_is_valid() -> None:
    """Test that the EO metadata registration asset is correctly defined."""
    assert isinstance(register_eo_stac_metadata, AssetsDefinition)
    asset_keys = [key.to_python_identifier() for key in register_eo_stac_metadata.keys]
    assert "register_eo_stac_metadata" in asset_keys


def test_eo_metadata_registration_dependencies() -> None:
    """Test that the EO metadata registration depends on the EO STAC asset."""
    input_keys = register_eo_stac_metadata.keys_by_input_name
    dep_names = [key.to_python_identifier() for key in input_keys.values()]
    assert "eo_stac_sentinel2_maharashtra" in dep_names
