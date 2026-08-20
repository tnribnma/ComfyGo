from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field, ConfigDict


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    code: str
    detail: Optional[str] = None


class TimestampedOut(BaseModel):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)