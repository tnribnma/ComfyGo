from sqlalchemy import String, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Flight(TimestampMixin, Base):
    __tablename__ = "flights"

    flight_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    airline: Mapped[str] = mapped_column(String(100), nullable=False)
    flight_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    departure_city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    arrival_city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    departure_airport: Mapped[str] = mapped_column(String(10), nullable=True)
    arrival_airport: Mapped[str] = mapped_column(String(10), nullable=True)
    departure_time: Mapped[str] = mapped_column(String(10), nullable=False)
    arrival_time: Mapped[str] = mapped_column(String(10), nullable=False)
    duration: Mapped[str] = mapped_column(String(20), nullable=False)
    stops: Mapped[str] = mapped_column(String(50), default="Direct")
    price_economy: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    price_business: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    price_first_class: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    cabin_class: Mapped[str] = mapped_column(String(50), default="Economy")
    baggage_allowance: Mapped[str] = mapped_column(String(50), nullable=True)
    total_seats: Mapped[int] = mapped_column(Integer, default=180)
    available_seats: Mapped[int] = mapped_column(Integer, default=180)
    image: Mapped[str] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<Flight id={self.flight_id} number={self.flight_number}>"
