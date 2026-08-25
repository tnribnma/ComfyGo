import enum
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    String, Integer, ForeignKey, Date, DateTime, Numeric, Enum as SAEnum, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .customer import Customer
    from .package import TourPackage


class PackageBookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PackageBooking(TimestampMixin, Base):
    __tablename__ = "package_bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)

    package_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tour_packages.package_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    travel_date: Mapped[date] = mapped_column(Date, nullable=False)
    num_persons: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    status: Mapped[PackageBookingStatus] = mapped_column(
        SAEnum(PackageBookingStatus, name="pkg_booking_status", native_enum=False),
        nullable=False, default=PackageBookingStatus.PENDING,
    )

    special_requests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dietary_requirements: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    contact_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    package: Mapped["TourPackage"] = relationship("TourPackage", back_populates="bookings")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="package_bookings")

    def __repr__(self) -> str:
        return (
            f"<PackageBooking id={self.id} ref={self.booking_ref} "
            f"package={self.package_id} status={self.status.value}>"
        )
