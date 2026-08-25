from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Room
from .base import GenericRepository


class RoomRepository(GenericRepository[Room]):
    model = Room

    def list_by_hotel(self, hotel_id: int, skip: int = 0, limit: int = 100) -> Sequence[Room]:
        stmt = (
            select(Room)
            .where(Room.hotel_id == hotel_id)
            .order_by(Room.price_per_night)
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def search(self, *, hotel_id: Optional[int] = None, min_price: Optional[float] = None,
               max_price: Optional[float] = None, skip: int = 0, limit: int = 50) -> Sequence[Room]:
        stmt = select(Room)
        if hotel_id:
            stmt = stmt.where(Room.hotel_id == hotel_id)
        if min_price is not None:
            stmt = stmt.where(Room.price_per_night >= min_price)
        if max_price is not None:
            stmt = stmt.where(Room.price_per_night <= max_price)
        stmt = stmt.order_by(Room.price_per_night).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()
