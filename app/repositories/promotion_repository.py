from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Promotion
from .base import GenericRepository


class PromotionRepository(GenericRepository[Promotion]):
    model = Promotion

    def list_active(self, skip: int = 0, limit: int = 50) -> Sequence[Promotion]:
        stmt = (
            select(Promotion)
            .where(Promotion.is_active == True)
            .order_by(Promotion.discount_percent.desc().nulls_last())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()
