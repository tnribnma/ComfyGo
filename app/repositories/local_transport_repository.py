from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import LocalTransport
from .base import GenericRepository


class LocalTransportRepository(GenericRepository[LocalTransport]):
    model = LocalTransport

    def search(self, *, transport_type: Optional[str] = None,
               departure_city: Optional[str] = None, arrival_city: Optional[str] = None,
               min_price: Optional[float] = None, max_price: Optional[float] = None,
               skip: int = 0, limit: int = 50) -> Sequence[LocalTransport]:
        stmt = select(LocalTransport).where(LocalTransport.is_active == True)
        if transport_type:
            stmt = stmt.where(LocalTransport.transport_type.ilike(f"%{transport_type}%"))
        if departure_city:
            stmt = stmt.where(LocalTransport.departure_city.ilike(f"%{departure_city}%"))
        if arrival_city:
            stmt = stmt.where(LocalTransport.arrival_city.ilike(f"%{arrival_city}%"))
        if min_price is not None:
            stmt = stmt.where(LocalTransport.price_per_person >= min_price)
        if max_price is not None:
            stmt = stmt.where(LocalTransport.price_per_person <= max_price)
        stmt = stmt.order_by(LocalTransport.price_per_person).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()
