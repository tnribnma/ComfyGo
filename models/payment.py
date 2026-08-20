import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    String, Integer, ForeignKey, Numeric, DateTime, Enum as SAEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .booking import Booking


class PaymentMethod(str, enum.Enum):
    CARD = "card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(TimestampMixin, Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    payment_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        SAEnum(PaymentMethod, name="payment_method", native_enum=False),
        nullable=False,
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SAEnum(PaymentStatus, name="payment_status", native_enum=False),
        nullable=False,
        default=PaymentStatus.PENDING,
    )
    transaction_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    booking_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )

    booking: Mapped["Booking"] = relationship("Booking", back_populates="payment")

    def __repr__(self) -> str:
        return (
            f"<Payment id={self.payment_id} amount={self.payment_amount} "
            f"status={self.payment_status.value if self.payment_status else None}>"
        )