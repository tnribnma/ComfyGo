import enum
from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    String, Integer, ForeignKey, Date, Numeric, Enum as SAEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .customer import Customer
    from .hotel import Hotel
    from .guide import Guide
    from .payment import Payment


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(TimestampMixin, Base):
    __tablename__ = "bookings"

    booking_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    booking_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    check_in_date: Mapped[date] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[date] = mapped_column(Date, nullable=False)
    number_of_guests: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    booking_status: Mapped[BookingStatus] = mapped_column(
        SAEnum(BookingStatus, name="booking_status", native_enum=False),
        nullable=False,
        default=BookingStatus.PENDING,
    )
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    hotel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("hotels.hotel_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    guide_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("guides.guide_id", ondelete="SET NULL"),
        nullable=True, index=True,
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="bookings")
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="bookings")
    guide: Mapped[Optional["Guide"]] = relationship("Guide", back_populates="bookings")
    payment: Mapped[Optional["Payment"]] = relationship(
        "Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Booking id={self.booking_id} customer={self.customer_id} "
            f"status={self.booking_status.value if self.booking_status else None}>"
        )