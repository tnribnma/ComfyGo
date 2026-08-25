from sqlalchemy import String, Integer, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class LocalTransport(TimestampMixin, Base):
    __tablename__ = "local_transports"

    transport_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transport_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)  
    provider_name: Mapped[str] = mapped_column(String(100), nullable=False)
    route_name: Mapped[str] = mapped_column(String(150), nullable=True) 
    departure_city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    arrival_city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    departure_time: Mapped[str] = mapped_column(String(10), nullable=True)
    arrival_time: Mapped[str] = mapped_column(String(10), nullable=True)
    duration: Mapped[str] = mapped_column(String(20), nullable=True)
    price_per_person: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    total_seats: Mapped[int] = mapped_column(Integer, default=40)
    available_seats: Mapped[int] = mapped_column(Integer, default=40)
    frequency: Mapped[str] = mapped_column(String(50), nullable=True)  
    features: Mapped[str] = mapped_column(String(500), nullable=True)  
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<LocalTransport id={self.transport_id} type={self.transport_type}>"
