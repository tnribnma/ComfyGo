from datetime import date
from typing import Optional, Sequence
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Booking, BookingStatus
from .base import GenericRepository


class BookingRepository(GenericRepository[Booking]):
    model = Booking

    def list_by_customer(
        self, customer_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Booking]:
        stmt = (
            select(Booking)
            .where(Booking.customer_id == customer_id)
            .order_by(Booking.booking_date.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_hotel(
        self, hotel_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Booking]:
        stmt = (
            select(Booking)
            .where(Booking.hotel_id == hotel_id)
            .order_by(Booking.check_in_date.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_guide(
        self, guide_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Booking]:
        stmt = (
            select(Booking)
            .where(Booking.guide_id == guide_id)
            .order_by(Booking.check_in_date.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_status(
        self, status: BookingStatus, skip: int = 0, limit: int = 100
    ) -> Sequence[Booking]:
        stmt = (
            select(Booking)
            .where(Booking.booking_status == status)
            .order_by(Booking.booking_date.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_date_range(
        self,
        start: date,
        end: date,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Booking]:
        stmt = (
            select(Booking)
            .where(
                Booking.check_in_date >= start,
                Booking.check_out_date <= end,
            )
            .order_by(Booking.check_in_date)
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def count_active_for_customer(self, customer_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Booking)
            .where(
                Booking.customer_id == customer_id,
                Booking.booking_status.in_(
                    [BookingStatus.PENDING, BookingStatus.CONFIRMED]
                ),
            )
        )
        return int(self.db.scalar(stmt) or 0)

    def has_overlapping(
        self,
        hotel_id: int,
        check_in: date,
        check_out: date,
        exclude_id: Optional[int] = None,
    ) -> bool:
        stmt = (
            select(Booking.booking_id)
            .where(
                Booking.hotel_id == hotel_id,
                Booking.booking_status != BookingStatus.CANCELLED,
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in,
            )
            .limit(1)
        )
        if exclude_id is not None:
            stmt = stmt.where(Booking.booking_id != exclude_id)
        return self.db.scalars(stmt).first() is not None