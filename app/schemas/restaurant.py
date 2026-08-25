from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut


class RestaurantBase(BaseModel):
    restaurant_name: str = Field(..., max_length=200)
    destination: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    cuisine: str = Field(..., max_length=100)
    description: Optional[str] = None
    price_range: Optional[str] = Field(default=None, max_length=10)
    rating: Optional[float] = None
    address: Optional[str] = None
    phone: Optional[str] = Field(default=None, max_length=30)
    website: Optional[str] = Field(default=None, max_length=300)
    opening_hours: Optional[str] = None
    popular_dishes: Optional[str] = None
    vegetarian_options: bool = False
    outdoor_seating: bool = False
    delivery_available: bool = False
    accepts_reservations: bool = False
    wifi: bool = False
    parking: bool = False
    live_music: bool = False
    is_featured: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image: Optional[str] = None
    images: Optional[str] = None  # JSON array of URLs


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    restaurant_name: Optional[str] = None
    destination: Optional[str] = None
    cuisine: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    price_range: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[str] = None
    popular_dishes: Optional[str] = None
    vegetarian_options: Optional[bool] = None
    outdoor_seating: Optional[bool] = None
    delivery_available: Optional[bool] = None
    accepts_reservations: Optional[bool] = None
    wifi: Optional[bool] = None
    parking: Optional[bool] = None
    live_music: Optional[bool] = None
    is_featured: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image: Optional[str] = None
    images: Optional[str] = None


class RestaurantOut(RestaurantBase, TimestampedOut):
    restaurant_id: int
    model_config = ConfigDict(from_attributes=True)


class RestaurantSummary(BaseModel):
    """Lightweight restaurant info for listings."""
    restaurant_id: int
    restaurant_name: str
    destination: str
    cuisine: str
    price_range: Optional[str] = None
    rating: Optional[float] = None
    image: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
