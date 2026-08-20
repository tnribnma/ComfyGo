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


class HotelOut(HotelBase, TimestampedOut):
    hotel_id: int
    model_config = ConfigDict(from_attributes=True)