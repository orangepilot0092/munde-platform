"""
Integration tests for Sprint 41 Batch 6 Connector Configurations.
Validates Government, Health, Education, Transport, and Economy YAML configs.
"""

from dagster import AssetsDefinition

from src.core.connectors.factory import load_connector_configs, create_ingest_asset

CONFIG_DIR = "configs/connectors"

BATCH_6_TARGETS = [
    "census_population_maharashtra",
    "udise_schools_maharashtra",
    "nhai_toll_plazas_maharashtra",
    "rbi_macroeconomic_maharashtra",
    "idsp_disease_outbreaks_maharashtra",
    "msrtc_bus_routes_maharashtra",
]


def test_batch_6_configs_load_successfully() -> None:
    """Test that all Batch 6 YAML files are valid and load without Pydantic errors."""
    configs = load_connector_configs(CONFIG_DIR)
    config_names = [cfg.name for cfg in configs]

    for target in BATCH_6_TARGETS:
        assert target in config_names, (
            f"Expected config '{target}' not found in loaded configs."
        )


def test_batch_6_assets_generate_successfully() -> None:
    """Test that the factory can generate Dagster assets for all Batch 6 configs."""
    configs = load_connector_configs(CONFIG_DIR)

    target_configs = [cfg for cfg in configs if cfg.name in BATCH_6_TARGETS]
    assert len(target_configs) == len(BATCH_6_TARGETS)

    for config in target_configs:
        asset_def = create_ingest_asset(config)
        assert isinstance(asset_def, AssetsDefinition)

        asset_keys = [key.to_python_identifier() for key in asset_def.keys]
        assert f"ingest_{config.name}" in asset_keys
