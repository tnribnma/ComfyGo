from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class LocalTransportBase(BaseModel):
    transport_type: str = Field(..., max_length=30, description="Bus, Train, Taxi, or Car Rental")
    provider_name: str = Field(..., max_length=100)
    route_name: Optional[str] = Field(default=None, max_length=150)
    departure_city: str = Field(..., max_length=100)
    arrival_city: str = Field(..., max_length=100)
    departure_time: Optional[str] = Field(default=None, max_length=10)
    arrival_time: Optional[str] = Field(default=None, max_length=10)
    duration: Optional[str] = Field(default=None, max_length=20)
    price_per_person: float = Field(..., ge=0)
    currency: str = "USD"
    total_seats: int = Field(default=40, ge=1)
    available_seats: int = Field(default=40, ge=0)
    frequency: Optional[str] = Field(default=None, max_length=50)
    features: Optional[str] = Field(default=None, max_length=500)
    image: Optional[str] = None


class LocalTransportCreate(LocalTransportBase):
    pass


class LocalTransportUpdate(BaseModel):
    transport_type: Optional[str] = None
    provider_name: Optional[str] = None
    route_name: Optional[str] = None
    departure_city: Optional[str] = None
    arrival_city: Optional[str] = None
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    duration: Optional[str] = None
    price_per_person: Optional[float] = None
    currency: Optional[str] = None
    total_seats: Optional[int] = None
    available_seats: Optional[int] = None
    frequency: Optional[str] = None
    features: Optional[str] = None
    image: Optional[str] = None


class LocalTransportBook(BaseModel):
    seats_to_book: int = Field(default=1, ge=1, le=10)


class LocalTransportOut(LocalTransportBase, TimestampedOut):
    transport_id: int
    model_config = ConfigDict(from_attributes=True)
