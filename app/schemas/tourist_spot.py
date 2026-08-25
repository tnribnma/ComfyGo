from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class TouristSpotBase(BaseModel):
    spot_name: str = Field(..., min_length=2, max_length=150)
    spot_city: str = Field(..., min_length=2, max_length=100)
    spot_country: str = Field(..., min_length=2, max_length=100)
    spot_description: Optional[str] = None
    spot_category: str = Field(default="attraction", max_length=50)
    spot_type: Optional[str] = None  # Beach, Temple, Park, Museum, etc.
    spot_rating: Optional[int] = Field(default=None, ge=0, le=5)
    spot_review_count: int = 0
    spot_detailed_description: Optional[str] = None
    spot_hero_image: Optional[str] = Field(default=None, max_length=500)
    spot_gallery_images: Optional[str] = None  # JSON array
    spot_best_time: Optional[str] = Field(default=None, max_length=200)
    spot_duration: Optional[str] = Field(default=None, max_length=200)
    spot_budget_daily: Optional[str] = Field(default=None, max_length=100)
    spot_currency: Optional[str] = Field(default=None, max_length=100)
    spot_language: Optional[str] = Field(default=None, max_length=200)
    spot_timezone: Optional[str] = Field(default=None, max_length=100)
    spot_weather: Optional[str] = None
    spot_latitude: Optional[float] = None
    spot_longitude: Optional[float] = None
    spot_opening_hours: Optional[str] = None
    spot_entry_fee: Optional[str] = None
    spot_accessibility: Optional[str] = None
    spot_facilities: Optional[str] = None  # JSON array
    spot_nearby_restaurants: Optional[str] = None  # JSON array
    spot_nearby_hotels: Optional[str] = None  # JSON array
    spot_things_to_do: Optional[str] = None  # JSON array
    spot_attractions: Optional[str] = None  # JSON array
    spot_activities: Optional[str] = None  # JSON array
    spot_nearby: Optional[str] = None  # JSON array
    spot_travel_tips: Optional[str] = None
    spot_safety_info: Optional[str] = None
    spot_transport_info: Optional[str] = None


class TouristSpotCreate(TouristSpotBase):
    pass


class TouristSpotUpdate(BaseModel):
    spot_name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    spot_city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    spot_country: Optional[str] = Field(default=None, min_length=2, max_length=100)
    spot_description: Optional[str] = None
    spot_category: Optional[str] = Field(default=None, max_length=50)
    spot_type: Optional[str] = None
    spot_rating: Optional[int] = Field(default=None, ge=0, le=5)
    spot_review_count: Optional[int] = None
    spot_detailed_description: Optional[str] = None
    spot_hero_image: Optional[str] = None
    spot_gallery_images: Optional[str] = None
    spot_best_time: Optional[str] = None
    spot_duration: Optional[str] = None
    spot_budget_daily: Optional[str] = None
    spot_currency: Optional[str] = None
    spot_language: Optional[str] = None
    spot_timezone: Optional[str] = None
    spot_weather: Optional[str] = None
    spot_latitude: Optional[float] = None
    spot_longitude: Optional[float] = None
    spot_opening_hours: Optional[str] = None
    spot_entry_fee: Optional[str] = None
    spot_accessibility: Optional[str] = None
    spot_facilities: Optional[str] = None
    spot_nearby_restaurants: Optional[str] = None
    spot_nearby_hotels: Optional[str] = None
    spot_things_to_do: Optional[str] = None
    spot_attractions: Optional[str] = None
    spot_activities: Optional[str] = None
    spot_nearby: Optional[str] = None
    spot_travel_tips: Optional[str] = None
    spot_safety_info: Optional[str] = None
    spot_transport_info: Optional[str] = None


class TouristSpotOut(TouristSpotBase, TimestampedOut):
    spot_id: int
    model_config = ConfigDict(from_attributes=True)
