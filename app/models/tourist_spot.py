from sqlalchemy import String, Integer, Text, Float, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class TouristSpot(TimestampMixin, Base):
    __tablename__ = "tourist_spots"

    spot_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    spot_name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    spot_city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    spot_country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    spot_description: Mapped[str] = mapped_column(Text, nullable=True)
    spot_category: Mapped[str] = mapped_column(String(50), nullable=False, default="attraction")
    spot_type: Mapped[str] = mapped_column(String(50), nullable=True) 
    spot_rating: Mapped[float] = mapped_column(Integer, nullable=True, default=0)
    spot_review_count: Mapped[int] = mapped_column(Integer, default=0)

    spot_detailed_description: Mapped[str] = mapped_column(Text, nullable=True)
    spot_hero_image: Mapped[str] = mapped_column(String(500), nullable=True)
    spot_gallery_images: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_best_time: Mapped[str] = mapped_column(String(200), nullable=True)
    spot_duration: Mapped[str] = mapped_column(String(200), nullable=True)
    spot_budget_daily: Mapped[str] = mapped_column(String(100), nullable=True)
    spot_currency: Mapped[str] = mapped_column(String(100), nullable=True)
    spot_language: Mapped[str] = mapped_column(String(200), nullable=True)
    spot_timezone: Mapped[str] = mapped_column(String(100), nullable=True)
    spot_weather: Mapped[str] = mapped_column(Text, nullable=True)
    spot_latitude: Mapped[float] = mapped_column(Float, nullable=True)
    spot_longitude: Mapped[float] = mapped_column(Float, nullable=True)
    spot_opening_hours: Mapped[str] = mapped_column(String(200), nullable=True)  
    spot_entry_fee: Mapped[str] = mapped_column(String(100), nullable=True)  
    spot_accessibility: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_facilities: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_nearby_restaurants: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_nearby_hotels: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_things_to_do: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_attractions: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_activities: Mapped[str] = mapped_column(Text, nullable=True)  
    spot_nearby: Mapped[str] = mapped_column(Text, nullable=True)   
    spot_travel_tips: Mapped[str] = mapped_column(Text, nullable=True)
    spot_safety_info: Mapped[str] = mapped_column(Text, nullable=True)
    spot_transport_info: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<TouristSpot id={self.spot_id} name={self.spot_name}>"
