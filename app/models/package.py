from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Integer, Numeric, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .customer import Customer
    from .package_booking import PackageBooking


class TourPackage(TimestampMixin, Base):
    __tablename__ = "tour_packages"

    package_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    package_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    destination: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_nights: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_person: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    original_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    included_services: Mapped[str] = mapped_column(Text, nullable=True)  
    excluded_services: Mapped[str] = mapped_column(Text, nullable=True)  
    itinerary: Mapped[str] = mapped_column(Text, nullable=True)  
    hotel_name: Mapped[str] = mapped_column(String(150), nullable=True)
    hotel_rating: Mapped[str] = mapped_column(String(20), nullable=True)  
    transportation: Mapped[str] = mapped_column(Text, nullable=True)
    meals: Mapped[str] = mapped_column(String(200), nullable=True) 
    tour_guide_included: Mapped[bool] = mapped_column(Boolean, default=True)
    tour_guide_name: Mapped[str] = mapped_column(String(150), nullable=True)
    group_size_min: Mapped[int] = mapped_column(Integer, default=2)
    group_size_max: Mapped[int] = mapped_column(Integer, default=15)
    booked_count: Mapped[int] = mapped_column(Integer, default=0)
    max_group_size: Mapped[int] = mapped_column(Integer, default=15)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=True)  
    available_dates: Mapped[str] = mapped_column(Text, nullable=True)  
    cancellation_policy: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=True)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    gallery_images: Mapped[str] = mapped_column(Text, nullable=True)  
    highlights: Mapped[str] = mapped_column(Text, nullable=True)  
    what_to_bring: Mapped[str] = mapped_column(Text, nullable=True)  
    languages: Mapped[str] = mapped_column(String(200), nullable=True)  # e.g. "English, Sinhala"

    bookings: Mapped[List["PackageBooking"]] = relationship("PackageBooking", back_populates="package")

    def __repr__(self) -> str:
        return f"<TourPackage id={self.package_id} name={self.package_name}>"
