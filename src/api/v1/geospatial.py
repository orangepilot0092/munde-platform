from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.geospatial import GeospatialService

router = APIRouter(prefix="/geospatial", tags=["Geospatial Analytics"])


@router.get("/districts/{name}/metrics")
def get_district_metrics(name: str, db: Session = Depends(get_db)):
    """Get the calculated area (sq km) and centroid (lat/lon) for a specific district."""
    service = GeospatialService(db)
    metrics = service.get_district_metrics(name)
    if not metrics:
        raise HTTPException(
            status_code=404, detail="District not found or missing geometry"
        )
    return metrics


@router.get("/districts/centroids")
def get_all_centroids(db: Session = Depends(get_db)):
    """Get centroids for all districts (Useful for map markers, clustering, and heatmaps)."""
    service = GeospatialService(db)
    return service.get_all_centroids()


@router.get("/districts/{name}/intersects")
def get_intersecting_features(name: str, db: Session = Depends(get_db)):
    """Find all spatial features that intersect (share a border) with a given district."""
    service = GeospatialService(db)
    return {"target": name, "intersections": service.find_intersecting_features(name)}
