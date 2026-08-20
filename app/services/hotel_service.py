from sqlalchemy.orm import Session

from ..repositories import HotelRepository
from ..schemas.hotel import HotelCreate, HotelUpdate

class HotelService:
    def __init__(self, db: Session):
        self.repo = HotelRepository(db)

    def get(self, hotel_id: int):
        return self.repo.get_or_404(hotel_id)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(skip=skip, limit=limit)

    def search(
        self, city=None, country=None,
        min_rating=None, max_rating=None,
        skip: int = 0, limit: int = 50,
    ):
        return self.repo.search(
            city=city, country=country,
            min_rating=min_rating, max_rating=max_rating,
            skip=skip, limit=limit,
        )

    def create(self, payload: HotelCreate):
        return self.repo.create(payload.model_dump())

    def update(self, hotel_id: int, payload: HotelUpdate):
        return self.repo.update(hotel_id, payload.model_dump(exclude_unset=True))

    def delete(self, hotel_id: int) -> None:
        self.repo.delete(hotel_id)