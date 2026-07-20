"""
Integration tests for Sprint 41 Batches 2 & 3 Connector Configurations.
Validates that Weather and Satellite YAML configs are syntactically valid and generate assets.
"""

from dagster import AssetsDefinition

from src.core.connectors.factory import load_connector_configs, create_ingest_asset

CONFIG_DIR = "configs/connectors"


def test_batches_2_3_configs_load_successfully() -> None:
    """Test that all Batch 2 & 3 YAML files are valid and load without Pydantic errors."""
    configs = load_connector_configs(CONFIG_DIR)

    # We now expect at least 13 configs (5 from Batch 1 + 8 from Batches 2 & 3)
    assert len(configs) >= 13, f"Expected at least 13 configs, found {len(configs)}"

    config_names = [cfg.name for cfg in configs]

    # Batch 2 Checks
    assert "census_population_maharashtra" in config_names
    assert "imd_observation_maharashtra" in config_names
    assert "noaa_gfs_maharashtra" in config_names
    assert "era5_climate_maharashtra" in config_names

    # Batch 3 Checks
    assert "stac_mpc_sentinel2_maharashtra" in config_names
    assert "stac_earthsearch_landsat_maharashtra" in config_names
    assert "stac_copernicus_sentinel1_maharashtra" in config_names
    assert "modis_ndvi_maharashtra" in config_names


def test_batches_2_3_assets_generate_successfully() -> None:
    """Test that the factory can generate Dagster assets for all Batch 2 & 3 configs."""
    configs = load_connector_configs(CONFIG_DIR)

    # Filter to just the new ones to test
    target_names = [
        "open_meteo_maharashtra",
        "imd_observation_maharashtra",
        "noaa_gfs_maharashtra",
        "era5_climate_maharashtra",
        "stac_mpc_sentinel2_maharashtra",
        "stac_earthsearch_landsat_maharashtra",
        "stac_copernicus_sentinel1_maharashtra",
        "modis_ndvi_maharashtra",
    ]

    for config in configs:
        if config.name in target_names:
            asset_def = create_ingest_asset(config)
            assert isinstance(asset_def, AssetsDefinition), (
                f"Failed to generate asset for {config.name}"
            )

            asset_keys = [key.to_python_identifier() for key in asset_def.keys]
            expected_key = f"ingest_{config.name}"
            assert expected_key in asset_keys, (
                f"Asset key {expected_key} not found for {config.name}"
            )
