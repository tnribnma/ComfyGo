from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .booking import Booking


class Customer(TimestampMixin, Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    customer_email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    customer_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    customer_password: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_address: Mapped[str] = mapped_column(Text, nullable=True)

    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Customer id={self.customer_id} email={self.customer_email}>"