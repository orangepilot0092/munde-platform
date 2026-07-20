import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text
from src.core.config import settings
from src.core.embeddings import EmbeddingService

engine = create_engine(settings.DATABASE_URL)
es = EmbeddingService()

with engine.connect() as conn:
    rows = conn.execute(
        text("SELECT dataset_id, name, description, domain FROM metadata_registry")
    ).fetchall()

    for row in rows:
        # Combine text fields for a rich embedding
        text_data = f"{row.name} {row.description or ''} {row.domain or ''}"
        vec = es.generate_embedding(text_data)

        # Format as string for raw SQL text() execution with pgvector
        vec_str = "[" + ",".join(str(x) for x in vec) + "]"

        conn.execute(
            text(
                "UPDATE metadata_registry SET embedding = :vec WHERE dataset_id = :id"
            ),
            {"vec": vec_str, "id": row.dataset_id},
        )
    conn.commit()

print(f"✅ Successfully backfilled embeddings for {len(rows)} datasets!")
