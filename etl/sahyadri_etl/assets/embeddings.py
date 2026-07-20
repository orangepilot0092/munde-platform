"""Dagster asset for batch embedding generation on DGX Spark AI Node."""

from __future__ import annotations

import logging
from typing import Any

from dagster import AssetExecutionContext, asset
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.providers.embeddings.local import LocalEmbeddingProvider

logger = logging.getLogger(__name__)

# Batch size for DB reads and embedding generation
DB_BATCH_SIZE = 100
EMBEDDING_BATCH_SIZE = 64


@asset(
    description="Generate embeddings for unembedded metadata_registry entries",
    group_name="embeddings",
    compute_kind="python",
)
def generate_metadata_embeddings(context: AssetExecutionContext) -> dict[str, Any]:
    """Batch-generate embeddings for metadata_registry rows where embedding IS NULL.

    This asset is designed to run on the DGX Spark AI Node. It:
    1. Reads unembedded rows in batches from PostgreSQL
    2. Generates embeddings via LocalEmbeddingProvider (GPU-accelerated)
    3. Writes vectors back to pgvector column
    4. Is idempotent: skips rows that already have embeddings

    Returns:
        Dict with processing statistics.
    """
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    provider = LocalEmbeddingProvider(batch_size=EMBEDDING_BATCH_SIZE)
    context.log.info(
        "Initialized %s (dimensions=%d)", provider.provider_name, provider.dimensions
    )

    total_processed = 0
    total_skipped = 0
    batch_num = 0

    try:
        while True:
            db = SessionLocal()
            try:
                # Read next batch of unembedded rows
                rows = db.execute(
                    text(
                        "SELECT dataset_id, name, description, domain "
                        "FROM metadata_registry "
                        "WHERE embedding IS NULL "
                        "ORDER BY dataset_id "
                        "LIMIT :limit OFFSET :offset"
                    ),
                    {"limit": DB_BATCH_SIZE, "offset": total_processed + total_skipped},
                ).fetchall()

                if not rows:
                    break

                batch_num += 1
                texts: list[str] = []
                dataset_ids: list[str] = []

                for row in rows:
                    # Combine name + description for richer semantic representation
                    text_parts = [row[1] or ""]  # name
                    if row[2]:  # description
                        text_parts.append(row[2])
                    if row[3]:  # domain
                        text_parts.append(f"[{row[3]}]")
                    combined = " ".join(text_parts).strip()
                    texts.append(combined)
                    dataset_ids.append(row[0])

                # Generate embeddings in batch (GPU-accelerated)
                embeddings = provider.generate_embeddings_batch(texts)

                # Write embeddings back to DB
                for ds_id, emb in zip(dataset_ids, embeddings):
                    db.execute(
                        text(
                            "UPDATE metadata_registry "
                            "SET embedding = CAST(:vec AS vector) "
                            "WHERE dataset_id = :id"
                        ),
                        {"vec": str(emb), "id": ds_id},
                    )

                db.commit()
                total_processed += len(rows)
                context.log.info(
                    "Batch %d: embedded %d rows (total: %d)",
                    batch_num,
                    len(rows),
                    total_processed,
                )

            finally:
                db.close()

    finally:
        engine.dispose()

    result = {
        "status": "success",
        "provider": provider.provider_name,
        "dimensions": provider.dimensions,
        "total_processed": total_processed,
        "total_skipped": total_skipped,
        "batches": batch_num,
    }
    context.log.info("Embedding generation complete: %s", result)
    return result
