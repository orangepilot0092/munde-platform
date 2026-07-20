from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.lineage import LineageService

router = APIRouter(prefix="/lineage", tags=["Data Provenance & Lineage"])


@router.get("/{dataset_id}")
def get_dataset_lineage(dataset_id: str, db: Session = Depends(get_db)):
    """
    Retrieve the complete ingestion history and provenance chain for a specific dataset.
    Traces the data from its official source URL, through the ETL connector, to the Data Lake.
    """
    service = LineageService(db)
    history = service.get_lineage(dataset_id)
    return {
        "dataset_id": dataset_id,
        "total_ingestions": len(history),
        "lineage_chain": history,
    }
