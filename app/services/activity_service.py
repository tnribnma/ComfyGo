from sqlalchemy.orm import Session
from ..repositories import ActivityRepository
from ..schemas.activity import ActivityCreate, ActivityUpdate


class ActivityService:
    def __init__(self, db: Session):
        self.repo = ActivityRepository(db)

    def get(self, activity_id: int):
        return self.repo.get_or_404(activity_id)

    def search(self, destination=None, category=None, min_price=None, max_price=None,
               difficulty=None, skip=0, limit=50):
        return self.repo.search(destination=destination, category=category, min_price=min_price,
                                max_price=max_price, difficulty=difficulty, skip=skip, limit=limit)

    def create(self, payload: ActivityCreate):
        return self.repo.create(payload.model_dump())

    def update(self, activity_id: int, payload: ActivityUpdate):
        return self.repo.update(activity_id, payload.model_dump(exclude_unset=True))

    def delete(self, activity_id: int) -> None:
        self.repo.delete(activity_id)
