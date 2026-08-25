from sqlalchemy import String, Integer, Numeric, Text, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Restaurant(TimestampMixin, Base):
    __tablename__ = "restaurants"

    restaurant_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    restaurant_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    destination: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    cuisine: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price_range: Mapped[str] = mapped_column(String(10), nullable=True) 
    rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=True)
    address: Mapped[str] = mapped_column(String(300), nullable=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    website: Mapped[str] = mapped_column(String(300), nullable=True)
    opening_hours: Mapped[str] = mapped_column(String(200), nullable=True)
    popular_dishes: Mapped[str] = mapped_column(Text, nullable=True)  
    vegetarian_options: Mapped[bool] = mapped_column(Boolean, default=False)
    outdoor_seating: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_available: Mapped[bool] = mapped_column(Boolean, default=False)
    accepts_reservations: Mapped[bool] = mapped_column(Boolean, default=False)
    wifi: Mapped[bool] = mapped_column(Boolean, default=False)
    parking: Mapped[bool] = mapped_column(Boolean, default=False)
    live_music: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    images: Mapped[str] = mapped_column(Text, nullable=True)  

    def __repr__(self) -> str:
        return f"<Restaurant id={self.restaurant_id} name={self.restaurant_name}>"
