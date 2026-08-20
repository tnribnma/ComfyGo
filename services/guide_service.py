from sqlalchemy.orm import Session

from ..repositories import GuideRepository
from ..schemas.guide import GuideCreate, GuideUpdate


class GuideService:
    def __init__(self, db: Session):
        self.repo = GuideRepository(db)

    def get(self, guide_id: int):
        return self.repo.get_or_404(guide_id)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(skip=skip, limit=limit)

    def list_by_language(self, language: str, skip: int = 0, limit: int = 100):
        return self.repo.list_by_language(language, skip=skip, limit=limit)

    def list_experienced(self, min_years: int = 5, skip: int = 0, limit: int = 100):
        return self.repo.list_by_experience_min(min_years, skip=skip, limit=limit)

    def top_guides(self, limit: int = 10):
        return self.repo.top_rated(limit=limit)

    def create(self, payload: GuideCreate):
        return self.repo.create(payload.model_dump())

    def update(self, guide_id: int, payload: GuideUpdate):
        return self.repo.update(guide_id, payload.model_dump(exclude_unset=True))

    def delete(self, guide_id: int) -> None:
        self.repo.delete(guide_id)