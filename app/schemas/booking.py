from datetime import date
from typing import Optional
from pydantic import (
    BaseModel, ConfigDict, Field, model_validator,
)

from .common import TimestampedOut
from ..models.booking import BookingStatus


class BookingBase(BaseModel):
    customer_id: int = Field(..., gt=0)
    hotel_id: int = Field(..., gt=0)
    guide_id: Optional[int] = Field(default=None, gt=0)
    booking_date: date
    check_in_date: date
    check_out_date: date
    number_of_guests: int = Field(default=1, ge=1, le=20)
    total_amount: float = Field(..., gt=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingBase":
        if self.check_out_date <= self.check_in_date:
            raise ValueError("check_out_date must be after check_in_date")
        if self.booking_date > self.check_in_date:
            raise ValueError("booking_date cannot be after check_in_date")
        return self


class BookingCreate(BookingBase):
    booking_status: BookingStatus = BookingStatus.PENDING


class BookingUpdate(BaseModel):
    customer_id: Optional[int] = Field(default=None, gt=0)
    hotel_id: Optional[int] = Field(default=None, gt=0)
    guide_id: Optional[int] = Field(default=None, gt=0)
    booking_date: Optional[date] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    number_of_guests: Optional[int] = Field(default=None, ge=1, le=20)
    booking_status: Optional[BookingStatus] = None
    total_amount: Optional[float] = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingUpdate":
        if self.check_in_date and self.check_out_date:
            if self.check_out_date <= self.check_in_date:
                raise ValueError("check_out_date must be after check_in_date")
        return self


class BookingOut(BookingBase, TimestampedOut):
    booking_id: int
    booking_status: BookingStatus
    model_config = ConfigDict(from_attributes=True)


class BookingStatusUpdate(BaseModel):
    """Lightweight DTO for status-only updates (e.g. confirm/cancel)."""
    booking_status: BookingStatus