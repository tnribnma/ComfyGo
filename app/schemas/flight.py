from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class FlightBase(BaseModel):
    airline: str = Field(..., max_length=100)
    flight_number: str = Field(..., max_length=20)
    departure_city: str = Field(..., max_length=100)
    arrival_city: str = Field(..., max_length=100)
    departure_airport: Optional[str] = Field(default=None, max_length=10)
    arrival_airport: Optional[str] = Field(default=None, max_length=10)
    departure_time: str = Field(..., max_length=10)
    arrival_time: str = Field(..., max_length=10)
    duration: str = Field(..., max_length=20)
    stops: str = "Direct"
    price_economy: float = Field(..., ge=0)
    price_business: Optional[float] = None
    price_first_class: Optional[float] = None
    cabin_class: str = "Economy"
    baggage_allowance: Optional[str] = None
    total_seats: int = Field(default=180, ge=1)
    available_seats: int = Field(default=180, ge=0)
    image: Optional[str] = None


class FlightCreate(FlightBase):
    pass


class FlightBookSeat(BaseModel):
    seats_to_book: int = Field(default=1, ge=1, le=9)
    cabin_class: str = Field(default="Economy", pattern="^(Economy|Business|First)$")


class FlightOut(FlightBase, TimestampedOut):
    flight_id: int
    model_config = ConfigDict(from_attributes=True)
