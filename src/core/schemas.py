from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = Field(..., ge=1)
    limit: int = Field(..., ge=1, le=100)
    total_items: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta


class StandardErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Any] = None
    request_id: Optional[str] = None
