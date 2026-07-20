"""
Integration tests for Sprint 41 Batches 4 & 5 Connector Configurations.
Validates GIS, Water, Agriculture, and Environment YAML configs.
"""

from dagster import AssetsDefinition

from src.core.connectors.factory import load_connector_configs, create_ingest_asset

CONFIG_DIR = "configs/connectors"

BATCH_4_5_TARGETS = [
    "geofabrik_maharashtra_osm",
    "overpass_api_maharashtra_waterbodies",
    "wrd_reservoir_levels_maharashtra",
    "cgwb_groundwater_maharashtra",
    "cpcb_aqi_maharashtra",
    "firms_fire_maharashtra",
    "soilgrids_maharashtra",
    "pmfby_claims_maharashtra",
]


def test_batches_4_5_configs_load_successfully() -> None:
    """Test that all Batch 4 & 5 YAML files are valid and load without Pydantic errors."""
    configs = load_connector_configs(CONFIG_DIR)
    config_names = [cfg.name for cfg in configs]

    for target in BATCH_4_5_TARGETS:
        assert target in config_names, (
            f"Expected config '{target}' not found in loaded configs."
        )


def test_batches_4_5_assets_generate_successfully() -> None:
    """Test that the factory can generate Dagster assets for all Batch 4 & 5 configs."""
    configs = load_connector_configs(CONFIG_DIR)

    target_configs = [cfg for cfg in configs if cfg.name in BATCH_4_5_TARGETS]
    assert len(target_configs) == len(BATCH_4_5_TARGETS)

    for config in target_configs:
        asset_def = create_ingest_asset(config)
        assert isinstance(asset_def, AssetsDefinition)

        asset_keys = [key.to_python_identifier() for key in asset_def.keys]
        assert f"ingest_{config.name}" in asset_keys
