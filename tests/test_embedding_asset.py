"""Integration tests for embedding generation logic.

Tests the core embedding pipeline without importing Dagster at module level,
avoiding Pydantic V2 incompatibility in Dagster's internal models.
"""

from __future__ import annotations

from typing import Any

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.providers.embeddings.mock import MockEmbeddingProvider


@pytest.fixture
def test_db() -> Any:
    """Create an in-memory SQLite database with metadata_registry schema."""
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    db.execute(
        text("""
        CREATE TABLE metadata_registry (
            dataset_id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            domain TEXT,
            embedding TEXT
        )
    """)
    )

    # Seed: 2 unembedded, 1 already embedded
    for row in [
        ("test_001", "Crop Production MH", "Annual crop data", "agriculture", None),
        ("test_002", "Rainfall Data MH", "District rainfall", "water", None),
        ("test_003", "Already Embedded", "Has vector", "health", "[0.1, 0.2]"),
    ]:
        db.execute(
            text(
                "INSERT INTO metadata_registry "
                "(dataset_id, name, description, domain, embedding) "
                "VALUES (:id, :name, :desc, :domain, :emb)"
            ),
            {
                "id": row[0],
                "name": row[1],
                "desc": row[2],
                "domain": row[3],
                "emb": row[4],
            },
        )
    db.commit()
    db.close()

    yield engine
    engine.dispose()


def _run_embedding_pipeline(
    engine: Any, provider: MockEmbeddingProvider
) -> dict[str, Any]:
    """Execute the embedding pipeline logic directly without Dagster decorator.

    Mirrors the logic in etl/sahyadri_etl/assets/embeddings.py but avoids
    importing the Dagster-decorated function at module level.
    """
    SessionLocal = sessionmaker(bind=engine)
    total_processed = 0
    batch_num = 0

    while True:
        db = SessionLocal()
        try:
            rows = db.execute(
                text(
                    "SELECT dataset_id, name, description, domain "
                    "FROM metadata_registry "
                    "WHERE embedding IS NULL "
                    "ORDER BY dataset_id "
                    "LIMIT :limit OFFSET :offset"
                ),
                {"limit": 100, "offset": total_processed},
            ).fetchall()

            if not rows:
                break

            batch_num += 1
            texts: list[str] = []
            dataset_ids: list[str] = []

            for row in rows:
                parts = [row[1] or ""]
                if row[2]:
                    parts.append(row[2])
                if row[3]:
                    parts.append(f"[{row[3]}]")
                texts.append(" ".join(parts).strip())
                dataset_ids.append(row[0])

            embeddings = provider.generate_embeddings_batch(texts)

            for ds_id, emb in zip(dataset_ids, embeddings):
                db.execute(
                    text(
                        "UPDATE metadata_registry "
                        "SET embedding = :vec "
                        "WHERE dataset_id = :id"
                    ),
                    {"vec": str(emb), "id": ds_id},
                )

            db.commit()
            total_processed += len(rows)
        finally:
            db.close()

    return {
        "status": "success",
        "provider": provider.provider_name,
        "dimensions": provider.dimensions,
        "total_processed": total_processed,
        "batches": batch_num,
    }


def test_embedding_pipeline_processes_unembedded_rows(test_db: Any) -> None:
    """Verify pipeline embeds only rows where embedding IS NULL."""
    provider = MockEmbeddingProvider(dimensions=8)
    result = _run_embedding_pipeline(test_db, provider)

    assert result["status"] == "success"
    assert result["total_processed"] == 2
    assert result["dimensions"] == 8

    SessionLocal = sessionmaker(bind=test_db)
    db = SessionLocal()
    rows = db.execute(
        text("SELECT dataset_id, embedding FROM metadata_registry ORDER BY dataset_id")
    ).fetchall()
    db.close()

    assert rows[0][1] is not None, "test_001 should have embedding"
    assert rows[1][1] is not None, "test_002 should have embedding"
    assert rows[2][1] == "[0.1, 0.2]", "test_003 should be unchanged"


def test_embedding_pipeline_is_idempotent(test_db: Any) -> None:
    """Verify re-running pipeline does not re-embed existing rows."""
    provider = MockEmbeddingProvider(dimensions=8)

    result1 = _run_embedding_pipeline(test_db, provider)
    result2 = _run_embedding_pipeline(test_db, provider)

    assert result1["total_processed"] == 2
    assert result2["total_processed"] == 0, "Second run should process 0 rows"
