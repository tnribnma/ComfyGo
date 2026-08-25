import enum
from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    String, Integer, ForeignKey, Date, Numeric, Enum as SAEnum, Text, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .customer import Customer
    from .activity import Activity


class ActivityBookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ActivityBooking(TimestampMixin, Base):
    __tablename__ = "activity_bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)

    activity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("activities.activity_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    num_persons: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    status: Mapped[ActivityBookingStatus] = mapped_column(
        SAEnum(ActivityBookingStatus, name="act_booking_status", native_enum=False),
        nullable=False, default=ActivityBookingStatus.PENDING,
    )

    special_requests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    dietary_requirements: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    participant_age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    health_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pick_up_location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    pick_up_time: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    activity: Mapped["Activity"] = relationship("Activity", back_populates="bookings")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="activity_bookings")

    def __repr__(self) -> str:
        return (
            f"<ActivityBooking id={self.id} ref={self.booking_ref} "
            f"activity={self.activity_id} status={self.status.value}>"
        )
