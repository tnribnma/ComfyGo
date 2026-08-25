from typing import Optional, Sequence
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from ..models import Restaurant
from .base import GenericRepository


class RestaurantRepository(GenericRepository[Restaurant]):
    model = Restaurant

    def search(
        self,
        *,
        destination: Optional[str] = None,
        cuisine: Optional[str] = None,
        min_rating: Optional[float] = None,
        price_range: Optional[str] = None,
        vegetarian: Optional[bool] = None,
        outdoor: Optional[bool] = None,
        delivery: Optional[bool] = None,
        reservations: Optional[bool] = None,
        wifi: Optional[bool] = None,
        featured: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Restaurant]:
        stmt = select(Restaurant)
        if destination:
            stmt = stmt.where(Restaurant.destination.ilike(f"%{destination}%"))
        if cuisine:
            stmt = stmt.where(Restaurant.cuisine.ilike(f"%{cuisine}%"))
        if min_rating is not None:
            stmt = stmt.where(Restaurant.rating >= min_rating)
        if price_range:
            stmt = stmt.where(Restaurant.price_range == price_range)
        if vegetarian:
            stmt = stmt.where(Restaurant.vegetarian_options == True)
        if outdoor:
            stmt = stmt.where(Restaurant.outdoor_seating == True)
        if delivery:
            stmt = stmt.where(Restaurant.delivery_available == True)
        if reservations:
            stmt = stmt.where(Restaurant.accepts_reservations == True)
        if wifi:
            stmt = stmt.where(Restaurant.wifi == True)
        if featured:
            stmt = stmt.where(Restaurant.is_featured == True)
        stmt = stmt.order_by(Restaurant.rating.desc().nulls_last()).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def top_restaurants(self, limit: int = 10) -> Sequence[Restaurant]:
        stmt = (
            select(Restaurant)
            .where(Restaurant.rating.isnot(None))
            .order_by(Restaurant.rating.desc())
            .limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_destinations(self) -> Sequence[Restaurant]:
        stmt = (
            select(Restaurant)
            .where(Restaurant.destination.isnot(None))
            .group_by(Restaurant.destination)
            .order_by(Restaurant.destination)
        )
        return self.db.scalars(stmt).all()

    def list_by_cuisine(self, cuisine: str, skip: int = 0, limit: int = 50) -> Sequence[Restaurant]:
        stmt = (
            select(Restaurant)
            .where(Restaurant.cuisine.ilike(f"%{cuisine}%"))
            .order_by(Restaurant.rating.desc().nulls_last())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def distinct_cuisines(self) -> list[str]:
        stmt = select(distinct(Restaurant.cuisine)).where(Restaurant.cuisine.isnot(None)).order_by(Restaurant.cuisine)
        return [row[0] for row in self.db.execute(stmt).all()]

    def distinct_destinations(self) -> list[str]:
        stmt = select(distinct(Restaurant.destination)).where(Restaurant.destination.isnot(None)).order_by(Restaurant.destination)
        return [row[0] for row in self.db.execute(stmt).all()]

    def count_by_destination(self) -> dict[str, int]:
        stmt = (
            select(Restaurant.destination, func.count(Restaurant.restaurant_id))
            .group_by(Restaurant.destination)
            .order_by(func.count(Restaurant.restaurant_id).desc())
        )
        return {dest: cnt for dest, cnt in self.db.execute(stmt).all()}
