from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .common import TimestampedOut
from ..models.activity_booking import ActivityBookingStatus


class ActivityBookingCreate(BaseModel):
    activity_id: int = Field(..., gt=0)
    booking_date: date
    num_persons: int = Field(..., ge=1, le=50)
    special_requests: Optional[str] = None
    dietary_requirements: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    participant_age: Optional[int] = None
    health_conditions: Optional[str] = None
    pick_up_location: Optional[str] = None
    pick_up_time: Optional[str] = None

    @field_validator("booking_date")
    @classmethod
    def date_must_be_future(cls, v: date) -> date:
        from datetime import date as _date
        if v < _date.today():
            raise ValueError("booking_date must be today or in the future")
        return v


class ActivityBookingUpdate(BaseModel):
    status: Optional[ActivityBookingStatus] = None
    special_requests: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    pick_up_location: Optional[str] = None
    pick_up_time: Optional[str] = None


class ActivityBookingOut(BaseModel):
    id: int
    booking_ref: str
    activity_id: int
    customer_id: int
    booking_date: date
    num_persons: int
    total_amount: float
    status: ActivityBookingStatus
    special_requests: Optional[str] = None
    dietary_requirements: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    participant_age: Optional[int] = None
    health_conditions: Optional[str] = None
    pick_up_location: Optional[str] = None
    pick_up_time: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
