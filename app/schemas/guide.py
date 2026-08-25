from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .common import TimestampedOut


class GuideBase(BaseModel):
    guide_name: str = Field(..., min_length=2, max_length=120)
    guide_email: EmailStr
    guide_phone: Optional[str] = Field(default=None, max_length=20)
    guide_city: Optional[str] = Field(default=None, max_length=100)
    guide_language: Optional[str] = Field(default=None, max_length=100)
    guide_experience: Optional[int] = Field(default=0, ge=0)
    bio: Optional[str] = None
    specialties: Optional[str] = Field(default=None, max_length=300)
    regions: Optional[str] = Field(default=None, max_length=300)
    hourly_rate: Optional[float] = Field(default=None, ge=0)
    daily_rate: Optional[float] = Field(default=None, ge=0)
    is_available: bool = True
    photo_url: Optional[str] = Field(default=None, max_length=500)
    whatsapp: Optional[str] = Field(default=None, max_length=30)
    facebook: Optional[str] = Field(default=None, max_length=200)
    instagram: Optional[str] = Field(default=None, max_length=200)


class GuideCreate(GuideBase):
    pass


class GuideUpdate(BaseModel):
    guide_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    guide_email: Optional[EmailStr] = None
    guide_phone: Optional[str] = Field(default=None, max_length=20)
    guide_city: Optional[str] = Field(default=None, max_length=100)
    guide_language: Optional[str] = Field(default=None, max_length=100)
    guide_experience: Optional[int] = Field(default=None, ge=0)
    bio: Optional[str] = None
    specialties: Optional[str] = Field(default=None, max_length=300)
    regions: Optional[str] = Field(default=None, max_length=300)
    hourly_rate: Optional[float] = Field(default=None, ge=0)
    daily_rate: Optional[float] = Field(default=None, ge=0)
    is_available: Optional[bool] = None
    photo_url: Optional[str] = Field(default=None, max_length=500)
    whatsapp: Optional[str] = Field(default=None, max_length=30)
    facebook: Optional[str] = Field(default=None, max_length=200)
    instagram: Optional[str] = Field(default=None, max_length=200)


class GuideOut(GuideBase, TimestampedOut):
    guide_id: int
    total_reviews: int = 0
    avg_rating: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)