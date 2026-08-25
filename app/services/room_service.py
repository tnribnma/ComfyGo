from sqlalchemy.orm import Session
from ..repositories import RoomRepository
from ..schemas.room import RoomCreate, RoomUpdate


class RoomService:
    def __init__(self, db: Session):
        self.repo = RoomRepository(db)

    def get(self, room_id: int):
        return self.repo.get_or_404(room_id)

    def list_by_hotel(self, hotel_id: int, skip=0, limit=100):
        return self.repo.list_by_hotel(hotel_id, skip=skip, limit=limit)

    def search(self, hotel_id=None, min_price=None, max_price=None, skip=0, limit=50):
        return self.repo.search(hotel_id=hotel_id, min_price=min_price, max_price=max_price, skip=skip, limit=limit)

    def create(self, payload: RoomCreate):
        return self.repo.create(payload.model_dump())

    def update(self, room_id: int, payload: RoomUpdate):
        return self.repo.update(room_id, payload.model_dump(exclude_unset=True))

    def delete(self, room_id: int) -> None:
        self.repo.delete(room_id)
