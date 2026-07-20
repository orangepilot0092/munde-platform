from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.search import SearchService
from src.core.limiter import limiter
from typing import Optional

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/unified")
@limiter.limit("5/minute")
def unified_search(
    request: Request,
    q: str = Query(..., description="Search query"),
    domain: Optional[str] = Query(None, description="Filter datasets by domain"),
    limit: int = Query(5, description="Max results per category"),
    db: Session = Depends(get_db),
):
    """
    Perform a unified hybrid search (Vector + Keyword) across datasets and documents.
    Rate limited to 5 requests per minute per IP.
    """
    service = SearchService(db)

    datasets = service.search_datasets(q, domain=domain, limit=limit)
    documents = service.search_documents_with_context(q, limit=limit)

    return {
        "query": q,
        "filters": {"domain": domain},
        "results": {"datasets": datasets, "documents": documents},
        "total_matches": len(datasets) + len(documents),
    }
