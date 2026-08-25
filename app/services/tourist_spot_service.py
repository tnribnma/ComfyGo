from sqlalchemy.orm import Session

from ..repositories import TouristSpotRepository
from ..schemas.tourist_spot import TouristSpotCreate, TouristSpotUpdate


class TouristSpotService:
    def __init__(self, db: Session):
        self.repo = TouristSpotRepository(db)

    def get(self, spot_id: int):
        return self.repo.get_or_404(spot_id)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(skip=skip, limit=limit)

    def search(self, city=None, country=None, category=None, skip: int = 0, limit: int = 50):
        return self.repo.search(city=city, country=country, category=category, skip=skip, limit=limit)

    def create(self, payload: TouristSpotCreate):
        return self.repo.create(payload.model_dump())

    def update(self, spot_id: int, payload: TouristSpotUpdate):
        return self.repo.update(spot_id, payload.model_dump(exclude_unset=True))

    def delete(self, spot_id: int) -> None:
        self.repo.delete(spot_id)
