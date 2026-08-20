from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Hotel
from .base import GenericRepository


class HotelRepository(GenericRepository[Hotel]):
    model = Hotel

    def get_by_email(self, email: str) -> Optional[Hotel]:
        stmt = select(Hotel).where(Hotel.hotel_email == email)
        return self.db.scalars(stmt).first()

    def list_by_city(self, city: str, skip: int = 0, limit: int = 100) -> Sequence[Hotel]:
        stmt = (
            select(Hotel)
            .where(Hotel.hotel_city.ilike(f"%{city}%"))
            .order_by(Hotel.hotel_rating.desc().nulls_last())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_country(self, country: str, skip: int = 0, limit: int = 100) -> Sequence[Hotel]:
        stmt = (
            select(Hotel)
            .where(Hotel.hotel_country.ilike(f"%{country}%"))
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def search(
        self,
        *,
        city: Optional[str] = None,
        country: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Hotel]:
        stmt = select(Hotel)
        if city:
            stmt = stmt.where(Hotel.hotel_city.ilike(f"%{city}%"))
        if country:
            stmt = stmt.where(Hotel.hotel_country.ilike(f"%{country}%"))
        if min_rating is not None:
            stmt = stmt.where(Hotel.hotel_rating >= min_rating)
        if max_rating is not None:
            stmt = stmt.where(Hotel.hotel_rating <= max_rating)
        stmt = (
            stmt.order_by(Hotel.hotel_rating.desc().nulls_last())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()