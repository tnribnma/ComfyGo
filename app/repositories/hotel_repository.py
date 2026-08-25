from typing import Optional, Sequence
from sqlalchemy import func, select, case
from sqlalchemy.orm import Session

from ..models import Hotel
from .base import GenericRepository


class HotelRepository(GenericRepository[Hotel]):
    model = Hotel

    def get_by_email(self, email: str) -> Optional[Hotel]:
        stmt = select(Hotel).where(Hotel.hotel_email == email)
        return self.db.scalars(stmt).first()

    def list_by_city(self, city: str, skip: int = 0, limit: int = 100) -> Sequence[Hotel]:
        stmt = (
            select(Hotel)
            .where(Hotel.hotel_city.ilike(f"%{city}%"))
            .order_by(Hotel.hotel_rating.desc().nulls_last())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_country(self, country: str, skip: int = 0, limit: int = 100) -> Sequence[Hotel]:
        stmt = (
            select(Hotel)
            .where(Hotel.hotel_country.ilike(f"%{country}%"))
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def search(
        self,
        *,
        city: Optional[str] = None,
        country: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        breakfast_included: Optional[bool] = None,
        has_pool: Optional[bool] = None,
        has_wifi: Optional[bool] = None,
        has_parking: Optional[bool] = None,
        free_cancellation: Optional[bool] = None,
        sort_by: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Hotel]:
        stmt = select(Hotel)
        if city:
            stmt = stmt.where(Hotel.hotel_city.ilike(f"%{city}%"))
        if country:
            stmt = stmt.where(Hotel.hotel_country.ilike(f"%{country}%"))
        if min_rating is not None:
            stmt = stmt.where(Hotel.hotel_rating >= min_rating)
        if max_rating is not None:
            stmt = stmt.where(Hotel.hotel_rating <= max_rating)
        if min_price is not None:
            stmt = stmt.where(Hotel.price_per_night >= min_price)
        if max_price is not None:
            stmt = stmt.where(Hotel.price_per_night <= max_price)
        if breakfast_included is not None:
            stmt = stmt.where(Hotel.breakfast_included == breakfast_included)
        if has_pool is not None:
            stmt = stmt.where(Hotel.has_pool == has_pool)
        if has_wifi is not None:
            stmt = stmt.where(Hotel.has_wifi == has_wifi)
        if has_parking is not None:
            stmt = stmt.where(Hotel.has_parking == has_parking)
        if free_cancellation is not None:
            stmt = stmt.where(Hotel.free_cancellation == free_cancellation)

        if sort_by == "price_asc":
            stmt = stmt.order_by(Hotel.price_per_night.asc().nulls_last())
        elif sort_by == "price_desc":
            stmt = stmt.order_by(Hotel.price_per_night.desc().nulls_last())
        elif sort_by == "rating":
            stmt = stmt.order_by(Hotel.hotel_rating.desc().nulls_last())
        elif sort_by == "name":
            stmt = stmt.order_by(Hotel.hotel_name.asc())
        else:
            stmt = stmt.order_by(Hotel.hotel_rating.desc().nulls_last())

        stmt = stmt.offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def list_destinations(self):
        stmt = (
            select(
                Hotel.hotel_city.label("city"),
                Hotel.hotel_country.label("country"),
                func.count(Hotel.hotel_id).label("hotel_count"),
            )
            .group_by(Hotel.hotel_city, Hotel.hotel_country)
            .order_by(func.count(Hotel.hotel_id).desc(), Hotel.hotel_city)
        )
        return [dict(row) for row in self.db.execute(stmt).mappings().all()]
