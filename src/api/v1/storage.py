from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.datalake_governance import DataLakeGovernance

router = APIRouter(prefix="/storage", tags=["Data Lake Governance"])


@router.post("/governance/apply")
def apply_governance_policies(db: Session = Depends(get_db)):
    """Apply versioning and lifecycle policies to core Data Lake buckets."""
    gov = DataLakeGovernance()
    buckets = ["documents", "agriculture", "backups"]
    results = []
    for b in buckets:
        try:
            gov.setup_bucket_governance(b)
            results.append({"bucket": b, "status": "configured"})
        except Exception as e:
            results.append({"bucket": b, "status": "error", "detail": str(e)})
    return {"message": "Governance policies applied", "results": results}


@router.get("/metrics")
def get_storage_metrics():
    """Get storage usage metrics for all MinIO buckets."""
    gov = DataLakeGovernance()
    return {"metrics": gov.get_storage_metrics()}
