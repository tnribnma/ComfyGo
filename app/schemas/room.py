from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class RoomBase(BaseModel):
    hotel_id: int
    room_type: str = Field(..., max_length=100)
    room_name: str = Field(..., max_length=150)
    room_description: Optional[str] = None
    room_capacity: Optional[str] = Field(default=None, max_length=50)
    room_beds: Optional[str] = Field(default=None, max_length=100)
    room_size_sqm: Optional[int] = None
    price_per_night: float = Field(..., gt=0)
    available_rooms: int = Field(default=5, ge=0)
    amenities: Optional[str] = None
    breakfast_included: bool = False
    images: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    room_type: Optional[str] = None
    room_name: Optional[str] = None
    room_description: Optional[str] = None
    room_capacity: Optional[str] = None
    room_beds: Optional[str] = None
    room_size_sqm: Optional[int] = None
    price_per_night: Optional[float] = None
    available_rooms: Optional[int] = None
    amenities: Optional[str] = None
    breakfast_included: Optional[bool] = None
    images: Optional[str] = None


class RoomOut(RoomBase, TimestampedOut):
    room_id: int
    model_config = ConfigDict(from_attributes=True)
