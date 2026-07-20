"""
Dagster Asset Factory for configuration-driven ingestion.
Reads YAML configs and dynamically generates Dagster @asset definitions.
"""

import logging
import os
from typing import Any, List

import yaml  # type: ignore[import-untyped]
from dagster import AssetExecutionContext, AssetsDefinition, MetadataValue, asset
from pydantic import TypeAdapter

from src.core.connectors.config import ConnectorConfig
from src.core.connectors.protocols.download import DownloadConnector
from src.core.connectors.protocols.rest import RESTConnector
from src.core.connectors.protocols.stac import STACConnector

logger = logging.getLogger(__name__)

# TypeAdapter for the discriminated union
connector_config_adapter: TypeAdapter[ConnectorConfig] = TypeAdapter(ConnectorConfig)


def load_connector_configs(config_dir: str) -> List[ConnectorConfig]:
    """Load and validate all YAML connector configurations from a directory."""
    configs: List[ConnectorConfig] = []
    if not os.path.exists(config_dir):
        logger.warning(f"Config directory {config_dir} does not exist.")
        return configs

    for filename in sorted(os.listdir(config_dir)):
        if filename.endswith((".yaml", ".yml")):
            filepath = os.path.join(config_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    # Validate against Pydantic schema using TypeAdapter
                    config = connector_config_adapter.validate_python(data)
                    configs.append(config)

    logger.info(
        f"✅ Loaded {len(configs)} valid connector configurations from {config_dir}"
    )
    return configs


def create_ingest_asset(config: ConnectorConfig) -> AssetsDefinition:
    """Factory function to create a Dagster asset for a specific connector config."""

    @asset(
        name=f"ingest_{config.name}",
        group_name=config.domain or "general",
        description=config.description or f"Ingestion asset for {config.name}",
    )
    async def dynamic_ingest_asset(context: AssetExecutionContext) -> None:
        context.log.info(f"🚀 Evaluating auto-generated ingestion for: {config.name}")

        # Respect Operational Status
        if config.status == "blocked":
            context.log.warning(
                f"🚫 BLOCKED: {config.name}. Reason: {config.blocked_reason}"
            )
            return
        if config.status == "ready":
            context.log.warning(
                f"🔐 READY: {config.name} is implemented but awaiting credentials/approval. Reason: {config.blocked_reason}"
            )
            return

        connector: Any = None
        result: Any = None

        if config.type == "rest":
            connector = RESTConnector(
                name=config.name,
                base_url=config.url,
                timeout=30.0,
                max_retries=3,
            )
            result = await connector.fetch_paginated(
                endpoint="",
                params=getattr(config, "params", {}),
                pagination_key=getattr(config, "pagination_key", None),
            )
        elif config.type == "stac":
            connector = STACConnector(
                name=config.name,
                catalog_url=config.catalog_url,
                timeout=60.0,
                max_retries=3,
            )
            result = await connector.search_items(
                collections=getattr(config, "collections", []),
                bbox=getattr(config, "bbox", None) or [72.5, 15.5, 81.0, 22.5],
                datetime_range=getattr(config, "datetime_range", None)
                or "2023-01-01/2024-01-01",
                limit=getattr(config, "limit", 50),
            )
        elif config.type == "download":
            connector = DownloadConnector(
                name=config.name,
                url=config.url,
                timeout=120.0,
                max_retries=3,
                destination_dir=getattr(config, "destination_dir", None),
            )
            result = await connector.fetch()
        else:
            context.log.warning(
                f"Connector type {config.type} not yet implemented in factory."
            )
            return

        if result and result.success:
            context.log.info(
                f"✅ Successfully ingested {result.records_processed} records for {config.name}"
            )
            context.add_output_metadata(
                {
                    "records_processed": MetadataValue.int(result.records_processed),
                    "quality_score": MetadataValue.float(result.quality_score),
                    "source_url": MetadataValue.text(
                        result.lineage.source_url or "unknown"
                    ),
                }
            )
        elif result:
            context.log.error(
                f"❌ Ingestion failed for {config.name}: {result.error_message}"
            )
            raise Exception(f"Ingestion failed: {result.error_message}")
        else:
            context.log.warning(f"⚠️ No result returned for {config.name}")

    return dynamic_ingest_asset


def load_and_generate_assets(config_dir: str) -> List[AssetsDefinition]:
    """Load YAML configs and generate Dagster assets."""
    configs = load_connector_configs(config_dir)
    return [create_ingest_asset(cfg) for cfg in configs]
