from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import TourPackage
from .base import GenericRepository


class TourPackageRepository(GenericRepository[TourPackage]):
    model = TourPackage

    def search(self, *, destination: Optional[str] = None, country: Optional[str] = None,
               min_price: Optional[float] = None, max_price: Optional[float] = None,
               difficulty: Optional[str] = None, skip: int = 0, limit: int = 50) -> Sequence[TourPackage]:
        stmt = select(TourPackage)
        if destination:
            stmt = stmt.where(TourPackage.destination.ilike(f"%{destination}%"))
        if country:
            stmt = stmt.where(TourPackage.country.ilike(f"%{country}%"))
        if min_price is not None:
            stmt = stmt.where(TourPackage.price_per_person >= min_price)
        if max_price is not None:
            stmt = stmt.where(TourPackage.price_per_person <= max_price)
        if difficulty:
            stmt = stmt.where(TourPackage.difficulty.ilike(f"%{difficulty}%"))
        stmt = stmt.order_by(TourPackage.rating.desc().nulls_last()).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()
