from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer, Numeric, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .activity_booking import ActivityBooking


class Activity(TimestampMixin, Base):
    __tablename__ = "activities"

    activity_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    destination: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    duration: Mapped[str] = mapped_column(String(100), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=True)  
    min_age: Mapped[int] = mapped_column(Integer, default=0)
    max_participants: Mapped[int] = mapped_column(Integer, default=20)
    booked_count: Mapped[int] = mapped_column(Integer, default=0)
    available_dates: Mapped[str] = mapped_column(Text, nullable=True) 
    cancellation_policy: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=True)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    gallery_images: Mapped[str] = mapped_column(Text, nullable=True) 
    category: Mapped[str] = mapped_column(String(50), nullable=True)  
    included: Mapped[str] = mapped_column(Text, nullable=True) 
    excluded: Mapped[str] = mapped_column(Text, nullable=True) 
    highlights: Mapped[str] = mapped_column(Text, nullable=True) 
    schedule: Mapped[str] = mapped_column(String(200), nullable=True)  
    what_to_bring: Mapped[str] = mapped_column(Text, nullable=True) 
    instructor_guide: Mapped[str] = mapped_column(String(150), nullable=True)
    languages: Mapped[str] = mapped_column(String(200), nullable=True)
    location_details: Mapped[str] = mapped_column(Text, nullable=True)
    safety_info: Mapped[str] = mapped_column(Text, nullable=True)
    fitness_level: Mapped[str] = mapped_column(String(50), nullable=True)

    bookings: Mapped[List["ActivityBooking"]] = relationship("ActivityBooking", back_populates="activity")

    def __repr__(self) -> str:
        return f"<Activity id={self.activity_id} name={self.activity_name}>"
