from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class ReviewBase(BaseModel):
    customer_id: int
    entity_type: str = Field(..., max_length=50)
    entity_id: int
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(default=None, max_length=200)
    comment: Optional[str] = None
    helpful_count: int = 0
    verified_visit: bool = False
    photos: Optional[str] = None
    owner_response: Optional[str] = None


class ReviewCreate(BaseModel):
    entity_type: str
    entity_id: int
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    comment: Optional[str] = None


class ReviewOut(ReviewBase, TimestampedOut):
    review_id: int
    model_config = ConfigDict(from_attributes=True)
