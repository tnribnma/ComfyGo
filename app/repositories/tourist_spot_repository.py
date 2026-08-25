from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import TouristSpot
from .base import GenericRepository


class TouristSpotRepository(GenericRepository[TouristSpot]):
    model = TouristSpot

    def list_by_city(self, city: str, skip: int = 0, limit: int = 100) -> Sequence[TouristSpot]:
        stmt = (
            select(TouristSpot)
            .where(TouristSpot.spot_city.ilike(f"%{city}%"))
            .order_by(TouristSpot.spot_name)
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_country(self, country: str, skip: int = 0, limit: int = 100) -> Sequence[TouristSpot]:
        stmt = (
            select(TouristSpot)
            .where(TouristSpot.spot_country.ilike(f"%{country}%"))
            .order_by(TouristSpot.spot_name)
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_category(self, category: str, skip: int = 0, limit: int = 100) -> Sequence[TouristSpot]:
        stmt = (
            select(TouristSpot)
            .where(TouristSpot.spot_category.ilike(f"%{category}%"))
            .order_by(TouristSpot.spot_name)
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def search(self, city: Optional[str] = None, country: Optional[str] = None,
               category: Optional[str] = None, skip: int = 0, limit: int = 50) -> Sequence[TouristSpot]:
        stmt = select(TouristSpot)
        if city:
            stmt = stmt.where(TouristSpot.spot_city.ilike(f"%{city}%"))
        if country:
            stmt = stmt.where(TouristSpot.spot_country.ilike(f"%{country}%"))
        if category:
            stmt = stmt.where(TouristSpot.spot_category.ilike(f"%{category}%"))
        stmt = stmt.order_by(TouristSpot.spot_name).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()
