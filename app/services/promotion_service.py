from sqlalchemy.orm import Session
from ..repositories import PromotionRepository
from ..schemas.promotion import PromotionCreate


class PromotionService:
    def __init__(self, db: Session):
        self.repo = PromotionRepository(db)

    def get(self, promotion_id: int):
        return self.repo.get_or_404(promotion_id)

    def list_active(self, skip=0, limit=50):
        return self.repo.list_active(skip=skip, limit=limit)

    def create(self, payload: PromotionCreate):
        return self.repo.create(payload.model_dump())

    def delete(self, promotion_id: int) -> None:
        self.repo.delete(promotion_id)
