from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any


class LineageService:
    def __init__(self, db: Session):
        self.db = db

    def record_event(
        self,
        dataset_id: str,
        connector_id: str,
        source_url: str,
        raw_storage_path: str,
        transformations: Dict[str, Any] = None,
    ):
        sql = text("""
            INSERT INTO data_lineage (dataset_id, connector_id, source_url, raw_storage_path, transformations)
            VALUES (:dataset_id, :connector_id, :source_url, :raw_storage_path, :transformations)
        """)
        import json

        self.db.execute(
            sql,
            {
                "dataset_id": dataset_id,
                "connector_id": connector_id,
                "source_url": source_url,
                "raw_storage_path": raw_storage_path,
                "transformations": json.dumps(transformations or {}),
            },
        )
        self.db.commit()

    def get_lineage(self, dataset_id: str) -> List[Dict]:
        sql = text("""
            SELECT id, dataset_id, connector_id, source_url, raw_storage_path, transformations, status, created_at
            FROM data_lineage
            WHERE dataset_id = :dataset_id
            ORDER BY created_at DESC
        """)
        res = self.db.execute(sql, {"dataset_id": dataset_id}).fetchall()
        return [
            {
                "event_id": r.id,
                "dataset_id": r.dataset_id,
                "connector_id": r.connector_id,
                "source_url": r.source_url,
                "raw_storage_path": r.raw_storage_path,
                "transformations": r.transformations,
                "status": r.status,
                "ingested_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in res
        ]
