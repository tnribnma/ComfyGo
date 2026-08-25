from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Activity
from .base import GenericRepository


class ActivityRepository(GenericRepository[Activity]):
    model = Activity

    def search(self, *, destination: Optional[str] = None, category: Optional[str] = None,
               min_price: Optional[float] = None, max_price: Optional[float] = None,
               difficulty: Optional[str] = None, skip: int = 0, limit: int = 50) -> Sequence[Activity]:
        stmt = select(Activity)
        if destination:
            stmt = stmt.where(Activity.destination.ilike(f"%{destination}%"))
        if category:
            stmt = stmt.where(Activity.category.ilike(f"%{category}%"))
        if min_price is not None:
            stmt = stmt.where(Activity.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Activity.price <= max_price)
        if difficulty:
            stmt = stmt.where(Activity.difficulty.ilike(f"%{difficulty}%"))
        stmt = stmt.order_by(Activity.rating.desc().nulls_last()).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()
