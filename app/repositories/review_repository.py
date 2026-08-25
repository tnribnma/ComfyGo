from typing import Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..models import Review
from .base import GenericRepository


class ReviewRepository(GenericRepository[Review]):
    model = Review

    def list_by_entity(self, entity_type: str, entity_id: int, skip: int = 0, limit: int = 100) -> Sequence[Review]:
        stmt = (
            select(Review)
            .where(Review.entity_type == entity_type, Review.entity_id == entity_id)
            .order_by(Review.created_at.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_customer(self, customer_id: int, skip: int = 0, limit: int = 100) -> Sequence[Review]:
        stmt = (
            select(Review)
            .where(Review.customer_id == customer_id)
            .order_by(Review.created_at.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def get_avg_rating(self, entity_type: str, entity_id: int) -> Optional[float]:
        stmt = select(func.avg(Review.rating)).where(
            Review.entity_type == entity_type, Review.entity_id == entity_id
        )
        return self.db.scalar(stmt)

    def get_count(self, entity_type: str, entity_id: int) -> int:
        stmt = select(func.count(Review.review_id)).where(
            Review.entity_type == entity_type, Review.entity_id == entity_id
        )
        return self.db.scalar(stmt) or 0
