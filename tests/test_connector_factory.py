"""
Integration tests for the configuration-driven connector factory.
"""

import os
import tempfile

from dagster import AssetsDefinition

from src.core.connectors.config import RESTConnectorConfig
from src.core.connectors.factory import create_ingest_asset, load_connector_configs


def test_load_connector_configs() -> None:
    """Test that YAML configs are loaded and validated correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_content = """
name: test_rest_api
type: rest
description: A test REST API
domain: testing
url: "https://api.example.com/data"
params:
  limit: 10
"""
        filepath = os.path.join(tmpdir, "test_api.yaml")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(yaml_content)

        configs = load_connector_configs(tmpdir)
        assert len(configs) == 1
        assert configs[0].name == "test_rest_api"
        assert configs[0].type == "rest"
        assert configs[0].params.get("limit") == 10


def test_create_ingest_asset() -> None:
    """Test that the factory creates a valid Dagster asset."""
    config = RESTConnectorConfig(
        name="test_asset",
        type="rest",
        url="https://api.example.com",
        domain="testing",
        schedule=None,
    )

    asset_def = create_ingest_asset(config)
    assert isinstance(asset_def, AssetsDefinition)

    asset_keys = [key.to_python_identifier() for key in asset_def.keys]
    assert "ingest_test_asset" in asset_keys
