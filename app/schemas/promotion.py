from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class PromotionBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    destination: Optional[str] = None
    original_price: Optional[float] = None
    discount_percent: Optional[int] = None
    final_price: Optional[float] = None
    promo_code: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    image: Optional[str] = None
    badge: Optional[str] = None
    is_active: bool = True


class PromotionCreate(PromotionBase):
    pass


class PromotionOut(PromotionBase, TimestampedOut):
    promotion_id: int
    model_config = ConfigDict(from_attributes=True)
