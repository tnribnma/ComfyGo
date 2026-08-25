from sqlalchemy import String, Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Room(TimestampMixin, Base):
    __tablename__ = "rooms"

    room_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(Integer, ForeignKey("hotels.hotel_id"), nullable=False, index=True)
    room_type: Mapped[str] = mapped_column(String(100), nullable=False)
    room_name: Mapped[str] = mapped_column(String(150), nullable=False)
    room_description: Mapped[str] = mapped_column(Text, nullable=True)
    room_capacity: Mapped[str] = mapped_column(String(50), nullable=True)  
    room_beds: Mapped[str] = mapped_column(String(100), nullable=True)  
    room_size_sqm: Mapped[int] = mapped_column(Integer, nullable=True)
    price_per_night: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    available_rooms: Mapped[int] = mapped_column(Integer, default=5)
    amenities: Mapped[str] = mapped_column(Text, nullable=True)  
    breakfast_included: Mapped[bool] = mapped_column(default=False)
    images: Mapped[str] = mapped_column(Text, nullable=True)  

    def __repr__(self) -> str:
        return f"<Room id={self.room_id} type={self.room_type}>"
