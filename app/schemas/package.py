from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class TourPackageBase(BaseModel):
    package_name: str = Field(..., max_length=200)
    destination: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    duration_days: int = Field(..., gt=0)
    duration_nights: int = Field(..., gt=0)
    price_per_person: float = Field(..., gt=0)
    original_price: Optional[float] = None
    description: Optional[str] = None
    included_services: Optional[str] = None
    excluded_services: Optional[str] = None
    itinerary: Optional[str] = None
    hotel_name: Optional[str] = None
    hotel_rating: Optional[str] = None
    transportation: Optional[str] = None
    meals: Optional[str] = None
    tour_guide_included: bool = True
    tour_guide_name: Optional[str] = None
    group_size_min: int = 2
    group_size_max: int = 15
    booked_count: int = 0
    max_group_size: int = 15
    difficulty: Optional[str] = None
    available_dates: Optional[str] = None
    cancellation_policy: Optional[str] = None
    rating: Optional[float] = None
    review_count: int = 0
    is_active: bool = True
    image: Optional[str] = None
    gallery_images: Optional[str] = None
    highlights: Optional[str] = None
    what_to_bring: Optional[str] = None
    languages: Optional[str] = None


class TourPackageCreate(TourPackageBase):
    pass


class TourPackageUpdate(BaseModel):
    package_name: Optional[str] = None
    destination: Optional[str] = None
    country: Optional[str] = None
    duration_days: Optional[int] = None
    duration_nights: Optional[int] = None
    price_per_person: Optional[float] = None
    original_price: Optional[float] = None
    description: Optional[str] = None
    included_services: Optional[str] = None
    excluded_services: Optional[str] = None
    itinerary: Optional[str] = None
    rating: Optional[float] = None
    image: Optional[str] = None
    hotel_name: Optional[str] = None
    hotel_rating: Optional[str] = None
    transportation: Optional[str] = None
    meals: Optional[str] = None
    tour_guide_included: Optional[bool] = None
    tour_guide_name: Optional[str] = None
    difficulty: Optional[str] = None
    cancellation_policy: Optional[str] = None
    highlights: Optional[str] = None
    what_to_bring: Optional[str] = None
    languages: Optional[str] = None
    is_active: Optional[bool] = None
    max_group_size: Optional[int] = None


class TourPackageOut(TourPackageBase, TimestampedOut):
    package_id: int
    model_config = ConfigDict(from_attributes=True)
