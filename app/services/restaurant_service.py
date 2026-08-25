from sqlalchemy.orm import Session
from ..repositories import RestaurantRepository
from ..schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    def __init__(self, db: Session):
        self.repo = RestaurantRepository(db)

    def get(self, restaurant_id: int):
        return self.repo.get_or_404(restaurant_id)

    def search(self, destination=None, cuisine=None, min_rating=None, price_range=None,
               vegetarian=None, outdoor=None, delivery=None, reservations=None, wifi=None,
               featured=None, skip=0, limit=50):
        return self.repo.search(
            destination=destination, cuisine=cuisine, min_rating=min_rating,
            price_range=price_range, vegetarian=vegetarian, outdoor=outdoor,
            delivery=delivery, reservations=reservations, wifi=wifi,
            featured=featured, skip=skip, limit=limit,
        )

    def top_restaurants(self, limit: int = 10):
        return self.repo.top_restaurants(limit=limit)

    def list_destinations(self):
        return self.repo.list_destinations()

    def list_by_cuisine(self, cuisine: str, skip=0, limit=50):
        return self.repo.list_by_cuisine(cuisine, skip=skip, limit=limit)

    def distinct_cuisines(self):
        return self.repo.distinct_cuisines()

    def distinct_destinations(self):
        return self.repo.distinct_destinations()

    def count_by_destination(self):
        return self.repo.count_by_destination()

    def create(self, payload: RestaurantCreate):
        return self.repo.create(payload.model_dump())

    def update(self, restaurant_id: int, payload: RestaurantUpdate):
        return self.repo.update(restaurant_id, payload.model_dump(exclude_unset=True))

    def delete(self, restaurant_id: int) -> None:
        self.repo.delete(restaurant_id)
