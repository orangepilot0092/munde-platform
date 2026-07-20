import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)

sql = """
CREATE TABLE IF NOT EXISTS data_lineage (
    id SERIAL PRIMARY KEY,
    dataset_id VARCHAR(255) NOT NULL,
    connector_id VARCHAR(255),
    source_url TEXT,
    raw_storage_path TEXT,
    transformations JSONB,
    status VARCHAR(50) DEFAULT 'SUCCESS',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lineage_dataset ON data_lineage(dataset_id);
CREATE INDEX IF NOT EXISTS idx_lineage_connector ON data_lineage(connector_id);
"""

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()
print("✅ data_lineage table created and indexed successfully!")
