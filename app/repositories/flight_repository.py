from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Flight
from .base import GenericRepository


class FlightRepository(GenericRepository[Flight]):
    model = Flight

    def search(self, *, departure_city: Optional[str] = None, arrival_city: Optional[str] = None,
               min_price: Optional[float] = None, max_price: Optional[float] = None,
               skip: int = 0, limit: int = 50) -> Sequence[Flight]:
        stmt = select(Flight)
        if departure_city:
            stmt = stmt.where(Flight.departure_city.ilike(f"%{departure_city}%"))
        if arrival_city:
            stmt = stmt.where(Flight.arrival_city.ilike(f"%{arrival_city}%"))
        if min_price is not None:
            stmt = stmt.where(Flight.price_economy >= min_price)
        if max_price is not None:
            stmt = stmt.where(Flight.price_economy <= max_price)
        stmt = stmt.order_by(Flight.price_economy).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()
