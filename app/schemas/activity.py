from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class ActivityBase(BaseModel):
    activity_name: str = Field(..., max_length=200)
    destination: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    description: Optional[str] = None
    duration: Optional[str] = None
    price: float = Field(..., gt=0)
    difficulty: Optional[str] = None
    min_age: int = 0
    max_participants: int = 20
    booked_count: int = 0
    available_dates: Optional[str] = None
    cancellation_policy: Optional[str] = None
    is_active: bool = True
    rating: Optional[float] = None
    review_count: int = 0
    image: Optional[str] = None
    gallery_images: Optional[str] = None
    category: Optional[str] = None
    included: Optional[str] = None
    excluded: Optional[str] = None
    highlights: Optional[str] = None
    schedule: Optional[str] = None
    what_to_bring: Optional[str] = None
    instructor_guide: Optional[str] = None
    languages: Optional[str] = None
    location_details: Optional[str] = None
    safety_info: Optional[str] = None
    fitness_level: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    activity_name: Optional[str] = None
    destination: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    difficulty: Optional[str] = None
    min_age: Optional[int] = None
    max_participants: Optional[int] = None
    category: Optional[str] = None
    included: Optional[str] = None
    excluded: Optional[str] = None
    highlights: Optional[str] = None
    schedule: Optional[str] = None
    what_to_bring: Optional[str] = None
    instructor_guide: Optional[str] = None
    languages: Optional[str] = None
    location_details: Optional[str] = None
    safety_info: Optional[str] = None
    fitness_level: Optional[str] = None
    cancellation_policy: Optional[str] = None
    is_active: Optional[bool] = None
    image: Optional[str] = None
    gallery_images: Optional[str] = None


class ActivityOut(ActivityBase, TimestampedOut):
    activity_id: int
    model_config = ConfigDict(from_attributes=True)
