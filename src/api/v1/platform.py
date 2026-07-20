from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.platform_health import PlatformHealthService

router = APIRouter(prefix="/platform", tags=["Platform Health & Observability"])


@router.get("/health")
def get_platform_health(db: Session = Depends(get_db)):
    """
    Comprehensive health check of all core Phase 3 infrastructure components.
    Pings PostgreSQL, Redis, MinIO, and OpenSearch.
    """
    service = PlatformHealthService(db)
    return service.get_health_report()


@router.get("/metrics")
def get_platform_metrics(db: Session = Depends(get_db)):
    """
    Aggregated metrics across the Data Atlas, Knowledge Graph, and Data Lake.
    Ideal for piping into Prometheus/Grafana dashboards.
    """
    service = PlatformHealthService(db)
    return service.get_platform_metrics()
