from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .common import TimestampedOut
from ..models.payment import PaymentMethod, PaymentStatus


class PaymentBase(BaseModel):
    booking_id: int = Field(..., gt=0)
    payment_amount: float = Field(..., gt=0)
    payment_method: PaymentMethod
    transaction_id: str = Field(..., min_length=6, max_length=100)


class PaymentCreate(PaymentBase):
    payment_status: PaymentStatus = PaymentStatus.PENDING


class PaymentUpdate(BaseModel):
    payment_amount: Optional[float] = Field(default=None, gt=0)
    payment_method: Optional[PaymentMethod] = None
    payment_status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = Field(default=None, min_length=6, max_length=100)


class PaymentOut(PaymentBase, TimestampedOut):
    payment_id: int
    payment_status: PaymentStatus
    payment_date: datetime
    model_config = ConfigDict(from_attributes=True)


class PaymentStatusUpdate(BaseModel):
    """Lightweight DTO for status-only updates."""
    payment_status: PaymentStatus