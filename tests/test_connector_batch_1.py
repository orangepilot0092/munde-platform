"""
Integration tests for Sprint 41 Batch 1 Connector Configurations.
Validates that all Tier 1 YAML configs are syntactically valid and generate assets.
"""

from dagster import AssetsDefinition

from src.core.connectors.factory import load_connector_configs, create_ingest_asset

CONFIG_DIR = "configs/connectors"


def test_batch_1_configs_load_successfully() -> None:
    """Test that all Batch 1 YAML files are valid and load without Pydantic errors."""
    configs = load_connector_configs(CONFIG_DIR)

    # We expect at least the 4 new ones + nasa_power + open_meteo = 6 configs
    assert len(configs) >= 5, f"Expected at least 5 configs, found {len(configs)}"

    config_names = [cfg.name for cfg in configs]
    assert "chirps_rainfall_maharashtra" in config_names
    assert "gbif_occurrence_maharashtra" in config_names
    assert "hydrosheds_basins_maharashtra" in config_names
    assert "datagov_agriculture_maharashtra" in config_names


def test_batch_1_assets_generate_successfully() -> None:
    """Test that the factory can generate Dagster assets for all Batch 1 configs."""
    configs = load_connector_configs(CONFIG_DIR)

    for config in configs:
        asset_def = create_ingest_asset(config)
        assert isinstance(asset_def, AssetsDefinition), (
            f"Failed to generate asset for {config.name}"
        )

        asset_keys = [key.to_python_identifier() for key in asset_def.keys]
        expected_key = f"ingest_{config.name}"
        assert expected_key in asset_keys, (
            f"Asset key {expected_key} not found for {config.name}"
        )
