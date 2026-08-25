from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import String, Integer, Numeric, Text, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .booking import Booking


class Guide(TimestampMixin, Base):
    __tablename__ = "guides"

    guide_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guide_name: Mapped[str] = mapped_column(String(120), nullable=False)
    guide_email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    guide_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    guide_city: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    guide_language: Mapped[str] = mapped_column(String(100), nullable=True)
    guide_experience: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    specialties: Mapped[Optional[str]] = mapped_column(String(300), nullable=True) 
    regions: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)  
    hourly_rate: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    daily_rate: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    whatsapp: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    facebook: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    instagram: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0)
    avg_rating: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), nullable=True)

    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="guide"
    )

    def __repr__(self) -> str:
        return f"<Guide id={self.guide_id} name={self.guide_name}>"