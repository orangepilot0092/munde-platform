from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.opensearch_service import OpenSearchService
from typing import Optional

router = APIRouter(prefix="/catalog", tags=["OpenSearch Catalog"])


@router.post("/sync")
def sync_catalog_to_opensearch(db: Session = Depends(get_db)):
    """Trigger a manual sync of the metadata registry to OpenSearch."""
    service = OpenSearchService()
    count = service.sync_catalog(db)
    return {"message": f"Successfully synced {count} datasets to OpenSearch"}


@router.get("/search")
def search_catalog(
    q: str = Query("", description="Search query"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
):
    """Perform faceted search over the dataset catalog using OpenSearch."""
    service = OpenSearchService()
    return service.faceted_search(q, domain)
