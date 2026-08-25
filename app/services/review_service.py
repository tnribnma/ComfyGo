from sqlalchemy.orm import Session
from ..repositories import ReviewRepository
from ..schemas.review import ReviewCreate


class ReviewService:
    def __init__(self, db: Session):
        self.repo = ReviewRepository(db)

    def get(self, review_id: int):
        return self.repo.get_or_404(review_id)

    def list_by_entity(self, entity_type: str, entity_id: int, skip=0, limit=100):
        return self.repo.list_by_entity(entity_type, entity_id, skip=skip, limit=limit)

    def list_by_customer(self, customer_id: int, skip=0, limit=100):
        return self.repo.list_by_customer(customer_id, skip=skip, limit=limit)

    def get_stats(self, entity_type: str, entity_id: int):
        return {
            "avg_rating": self.repo.get_avg_rating(entity_type, entity_id),
            "total_reviews": self.repo.get_count(entity_type, entity_id),
        }

    def create(self, customer_id: int, payload: ReviewCreate):
        data = payload.model_dump()
        data["customer_id"] = customer_id
        return self.repo.create(data)

    def delete(self, review_id: int) -> None:
        self.repo.delete(review_id)
