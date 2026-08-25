from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .common import TimestampedOut


class HotelBase(BaseModel):
    hotel_name: str = Field(..., min_length=2, max_length=150)
    hotel_address: str = Field(..., min_length=5, max_length=255)
    hotel_city: str = Field(..., min_length=2, max_length=100)
    hotel_country: str = Field(..., min_length=2, max_length=100)
    hotel_phone: Optional[str] = Field(default=None, max_length=20)
    hotel_email: Optional[EmailStr] = None
    hotel_description: Optional[str] = None
    hotel_rating: Optional[float] = Field(default=None, ge=0, le=5)
    price_per_night: Optional[float] = Field(default=None, ge=0)
    breakfast_included: bool = False
    free_cancellation: bool = False
    has_pool: bool = False
    has_wifi: bool = False
    has_parking: bool = False


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    hotel_name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    hotel_address: Optional[str] = Field(default=None, min_length=5, max_length=255)
    hotel_city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    hotel_country: Optional[str] = Field(default=None, min_length=2, max_length=100)
    hotel_phone: Optional[str] = Field(default=None, max_length=20)
    hotel_email: Optional[EmailStr] = None
    hotel_description: Optional[str] = None
    hotel_rating: Optional[float] = Field(default=None, ge=0, le=5)
    price_per_night: Optional[float] = Field(default=None, ge=0)
    breakfast_included: Optional[bool] = None
    free_cancellation: Optional[bool] = None
    has_pool: Optional[bool] = None
    has_wifi: Optional[bool] = None
    has_parking: Optional[bool] = None


class HotelOut(HotelBase, TimestampedOut):
    hotel_id: int
    model_config = ConfigDict(from_attributes=True)


class DestinationOut(BaseModel):
    city: str
    country: str
    hotel_count: int
