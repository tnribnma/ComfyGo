from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .common import TimestampedOut
from ..models.package_booking import PackageBookingStatus


class PackageBookingCreate(BaseModel):
    package_id: int = Field(..., gt=0)
    travel_date: date
    num_persons: int = Field(..., ge=1, le=50)
    special_requests: Optional[str] = None
    dietary_requirements: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_contact: Optional[str] = None

    @field_validator("travel_date")
    @classmethod
    def date_must_be_future(cls, v: date) -> date:
        from datetime import date as _date
        if v < _date.today():
            raise ValueError("travel_date must be today or in the future")
        return v


class PackageBookingUpdate(BaseModel):
    status: Optional[PackageBookingStatus] = None
    special_requests: Optional[str] = None
    dietary_requirements: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_contact: Optional[str] = None


class PackageBookingOut(BaseModel):
    id: int
    booking_ref: str
    package_id: int
    customer_id: int
    travel_date: date
    num_persons: int
    total_amount: float
    status: PackageBookingStatus
    special_requests: Optional[str] = None
    dietary_requirements: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class PackageBookingOutFull(PackageBookingOut, TimestampedOut):
    """Booking output with package details embedded."""
    package_name: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    duration_nights: Optional[int] = None
    price_per_person: Optional[float] = None
    image: Optional[str] = None
