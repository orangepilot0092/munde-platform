from sqlalchemy import text
from sqlalchemy.orm import Session
from src.core.embeddings import EmbeddingService


class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.es = EmbeddingService()

    def _rrf_fusion(
        self, vector_results: list[dict], keyword_results: list[dict], k: int = 60
    ) -> list[dict]:
        scores = {}
        for rank, item in enumerate(vector_results):
            doc_id = item["id"]
            scores[doc_id] = scores.get(doc_id, 0) + (1.0 / (k + rank + 1))
            item["score"] = scores[doc_id]
        for rank, item in enumerate(keyword_results):
            doc_id = item["id"]
            scores[doc_id] = scores.get(doc_id, 0) + (1.0 / (k + rank + 1))
            item["score"] = scores[doc_id]

        all_items = {item["id"]: item for item in vector_results}
        for item in keyword_results:
            if item["id"] not in all_items:
                all_items[item["id"]] = item
        return sorted(all_items.values(), key=lambda x: x["score"], reverse=True)

    def search_datasets(
        self, query: str, domain: str = None, limit: int = 5
    ) -> list[dict]:
        query_vector = self.es.generate_embedding(query)

        # Vector Search (Relies on English embeddings)
        vec_sql = text("""
            SELECT dataset_id as id, name, name_mr, description, domain, 1 - (embedding <=> CAST(:vec AS vector)) as vec_score
            FROM metadata_registry 
            WHERE embedding IS NOT NULL AND (:domain IS NULL OR domain = :domain)
            ORDER BY embedding <=> CAST(:vec AS vector) LIMIT :limit
        """)
        vec_res = self.db.execute(
            vec_sql, {"vec": query_vector, "domain": domain, "limit": limit}
        ).fetchall()

        # Keyword Search (Uses 'simple' tsvector to support Devanagari exact matches)
        kw_sql = text("""
            SELECT dataset_id as id, name, name_mr, description, domain, ts_rank(search_vector, plainto_tsquery('simple', :query)) as kw_score
            FROM metadata_registry 
            WHERE search_vector @@ plainto_tsquery('simple', :query) AND (:domain IS NULL OR domain = :domain)
            ORDER BY kw_score DESC LIMIT :limit
        """)
        kw_res = self.db.execute(
            kw_sql, {"query": query, "domain": domain, "limit": limit}
        ).fetchall()

        v_items = [
            {
                "id": r.id,
                "name": r.name,
                "name_mr": r.name_mr,
                "description": r.description,
                "domain": r.domain,
                "type": "dataset",
            }
            for r in vec_res
        ]
        k_items = [
            {
                "id": r.id,
                "name": r.name,
                "name_mr": r.name_mr,
                "description": r.description,
                "domain": r.domain,
                "type": "dataset",
            }
            for r in kw_res
        ]
        return self._rrf_fusion(v_items, k_items)[:limit]

    def search_documents_with_context(self, query: str, limit: int = 3) -> list[dict]:
        # Document search remains unchanged for now
        query_vector = self.es.generate_embedding(query)
        sql = text("""
            WITH vector_match AS (
                SELECT id, document_id, chunk_index, content, 1 - (embedding <=> CAST(:vec AS vector)) as score
                FROM document_chunks WHERE embedding IS NOT NULL ORDER BY embedding <=> CAST(:vec AS vector) LIMIT :limit
            ),
            keyword_match AS (
                SELECT id, document_id, chunk_index, content, ts_rank(search_vector, plainto_tsquery('english', :query)) as score
                FROM document_chunks WHERE search_vector @@ plainto_tsquery('english', :query) ORDER BY score DESC LIMIT :limit
            )
            SELECT * FROM vector_match UNION SELECT * FROM keyword_match ORDER BY score DESC LIMIT :limit
        """)
        matches = self.db.execute(
            sql, {"vec": query_vector, "query": query, "limit": limit}
        ).fetchall()

        results = []
        for match in matches:
            ctx_sql = text("""
                SELECT chunk_index, content FROM document_chunks 
                WHERE document_id = :doc_id AND chunk_index BETWEEN :start AND :end ORDER BY chunk_index
            """)
            ctx_res = self.db.execute(
                ctx_sql,
                {
                    "doc_id": match.document_id,
                    "start": match.chunk_index - 1,
                    "end": match.chunk_index + 1,
                },
            ).fetchall()
            context_text = "\n".join([r.content for r in ctx_res])
            results.append(
                {
                    "type": "document_chunk",
                    "document_id": match.document_id,
                    "chunk_index": match.chunk_index,
                    "matched_text": match.content,
                    "context_window": context_text,
                    "score": float(match.score),
                }
            )
        return results
