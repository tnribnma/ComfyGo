from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import String, Integer, Numeric, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .employee import Employee
    from .booking import Booking


class Hotel(TimestampMixin, Base):
    __tablename__ = "hotels"

    hotel_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    hotel_address: Mapped[str] = mapped_column(String(255), nullable=False)
    hotel_city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    hotel_country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    hotel_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    hotel_email: Mapped[str] = mapped_column(String(150), nullable=True)
    hotel_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hotel_rating: Mapped[Optional[float]] = mapped_column(
        Numeric(2, 1), nullable=True 
    )

    employees: Mapped[List["Employee"]] = relationship(
        "Employee", back_populates="hotel"
    )
    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="hotel"
    )

    def __repr__(self) -> str:
        return f"<Hotel id={self.hotel_id} name={self.hotel_name}>"