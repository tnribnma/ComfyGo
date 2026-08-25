from typing import Optional, Sequence
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..models.activity_booking import ActivityBooking, ActivityBookingStatus
from .base import GenericRepository


class ActivityBookingRepository(GenericRepository[ActivityBooking]):
    model = ActivityBooking

    def generate_booking_ref(self) -> str:
        """Generate a unique booking reference like ACT-20260824-A1B2."""
        count = self.db.scalar(
            select(func.count()).select_from(ActivityBooking)
        ) or 0
        import random, string
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"ACT-{date.today().strftime('%Y%m%d')}-{suffix}"

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 50) -> Sequence[ActivityBooking]:
        stmt = (
            select(ActivityBooking)
            .where(ActivityBooking.customer_id == customer_id)
            .order_by(ActivityBooking.id.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def count_booked_for_date(self, activity_id: int, booking_date: date) -> int:
        """Count total persons booked for a specific activity on a specific date."""
        result = self.db.scalar(
            select(func.coalesce(func.sum(ActivityBooking.num_persons), 0)).where(
                ActivityBooking.activity_id == activity_id,
                ActivityBooking.booking_date == booking_date,
                ActivityBooking.status.in_([
                    ActivityBookingStatus.PENDING,
                    ActivityBookingStatus.CONFIRMED,
                ]),
            )
        )
        return int(result or 0)
