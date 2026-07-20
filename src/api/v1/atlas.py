from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.core.database import get_db
from src.schemas.atlas import DatasetSummary, DatasetDetail
from typing import List, Optional
import json

router = APIRouter(prefix="/atlas", tags=["Maharashtra Data Atlas"])


@router.get("/datasets", response_model=List[DatasetSummary])
def list_datasets(
    domain: Optional[str] = Query(None),
    min_quality: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT dataset_id, name, name_mr, name_hi, domain, quality_score, last_updated, tags
        FROM metadata_registry
        WHERE (:domain IS NULL OR domain = :domain)
          AND (:min_quality IS NULL OR quality_score >= :min_quality)
        ORDER BY quality_score DESC NULLS LAST, name ASC
        LIMIT :limit OFFSET :skip
    """)

    results = db.execute(
        query,
        {"domain": domain, "min_quality": min_quality, "limit": limit, "skip": skip},
    ).fetchall()

    return [
        DatasetSummary(
            dataset_id=r.dataset_id,
            name=r.name,
            name_mr=r.name_mr,
            name_hi=r.name_hi,
            domain=r.domain,
            quality_score=r.quality_score,
            last_updated=r.last_updated,
            tags=r.tags
            if isinstance(r.tags, list)
            else (json.loads(r.tags) if r.tags else None),
        )
        for r in results
    ]


@router.get("/datasets/{dataset_id}")
def get_dataset_details(
    dataset_id: str,
    lang: str = Query(
        "en", regex="^(en|mr|hi)$", description="Preferred language (en, mr, hi)"
    ),
    db: Session = Depends(get_db),
):
    """Retrieve dataset details. Dynamically returns localized name/description based on 'lang'."""
    query = text("SELECT * FROM metadata_registry WHERE dataset_id = :id")
    result = db.execute(query, {"id": dataset_id}).first()

    if not result:
        raise HTTPException(status_code=404, detail="Dataset not found in the Atlas")

    row_dict = result._asdict()

    # Localization Logic: Fallback to English if requested language is null
    if lang == "mr":
        row_dict["name"] = row_dict.get("name_mr") or row_dict["name"]
        row_dict["description"] = row_dict.get("description_mr") or row_dict.get(
            "description"
        )
    elif lang == "hi":
        row_dict["name"] = row_dict.get("name_hi") or row_dict["name"]
        row_dict["description"] = row_dict.get("description_hi") or row_dict.get(
            "description"
        )

    if row_dict.get("tags") and isinstance(row_dict["tags"], str):
        try:
            row_dict["tags"] = json.loads(row_dict["tags"])
        except Exception:
            pass

    return DatasetDetail(**row_dict)
