from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from sahyadri.core.database import get_db
from sahyadri.core.models import IntelligenceAsset
from sahyadri.api.schemas import AssetCreate, AssetResponse

router = APIRouter(prefix="/assets", tags=["Intelligence Assets"])

@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(asset_in: AssetCreate, db: AsyncSession = Depends(get_db)):
    db_asset = IntelligenceAsset(**asset_in.model_dump())
    db.add(db_asset)
    await db.commit()
    await db.refresh(db_asset)
    return db_asset

@router.get("/", response_model=List[AssetResponse])
async def list_assets(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(IntelligenceAsset).offset(skip).limit(limit))
    return result.scalars().all()
