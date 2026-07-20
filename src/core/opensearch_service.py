import os
from opensearchpy import OpenSearch
from sqlalchemy.orm import Session
from sqlalchemy import text


class OpenSearchService:
    def __init__(self):
        host = os.getenv("OPENSEARCH_HOST", "localhost")
        self.client = OpenSearch(
            hosts=[{"host": host, "port": 9200, "scheme": "http"}],
            use_ssl=False,
            verify_certs=False,
        )
        self.index_name = "sahyadri_catalog"
        self._ensure_index()

    def _ensure_index(self):
        if not self.client.indices.exists(index=self.index_name):
            mapping = {
                "mappings": {
                    "properties": {
                        "dataset_id": {"type": "keyword"},
                        "name": {
                            "type": "text",
                            "fields": {"raw": {"type": "keyword"}},
                        },
                        "description": {"type": "text"},
                        "domain": {"type": "keyword"},
                        "tags": {"type": "keyword"},
                        "quality_score": {"type": "float"},
                        "last_updated": {"type": "date"},
                    }
                }
            }
            self.client.indices.create(index=self.index_name, body=mapping)

    def sync_catalog(self, db: Session):
        """Sync PostgreSQL metadata_registry to OpenSearch."""
        query = text(
            "SELECT dataset_id, name, description, domain, tags, quality_score, last_updated FROM metadata_registry"
        )
        rows = db.execute(query).fetchall()

        for row in rows:
            tags = row.tags if isinstance(row.tags, list) else []

            doc = {
                "dataset_id": row.dataset_id,
                "name": row.name,
                "description": row.description,
                "domain": row.domain,
                "tags": tags,
                "quality_score": float(row.quality_score) if row.quality_score else 0.0,
                "last_updated": row.last_updated.isoformat()
                if row.last_updated
                else None,
            }
            self.client.index(index=self.index_name, id=row.dataset_id, body=doc)

        self.client.indices.refresh(index=self.index_name)
        return len(rows)

    def faceted_search(self, query: str, domain: str = None):
        """Perform multi-match search with domain aggregations (facets)."""
        must_clauses = []
        if query:
            must_clauses.append(
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["name^3", "description", "tags"],
                    }
                }
            )
        if domain:
            must_clauses.append({"term": {"domain": domain}})

        search_body = {
            "query": {"bool": {"must": must_clauses}}
            if must_clauses
            else {"match_all": {}},
            "aggs": {
                "domains": {"terms": {"field": "domain", "size": 10}},
                "avg_quality": {"avg": {"field": "quality_score"}},
            },
        }

        res = self.client.search(index=self.index_name, body=search_body)

        hits = [hit["_source"] for hit in res["hits"]["hits"]]
        aggs = res.get("aggregations", {})

        return {
            "total": res["hits"]["total"]["value"],
            "results": hits,
            "facets": {
                "domains": aggs.get("domains", {}).get("buckets", []),
                "avg_quality": aggs.get("avg_quality", {}).get("value"),
            },
        }
