from typing import Optional, Sequence
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..models.package_booking import PackageBooking, PackageBookingStatus
from ..models.package import TourPackage
from .base import GenericRepository


class PackageBookingRepository(GenericRepository[PackageBooking]):
    model = PackageBooking

    def generate_booking_ref(self) -> str:
        """Generate a unique booking reference like PKG-20260824-A1B2."""
        count = self.db.scalar(
            select(func.count()).select_from(PackageBooking)
        ) or 0
        import random, string
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"PKG-{date.today().strftime('%Y%m%d')}-{suffix}"

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 50) -> Sequence[PackageBooking]:
        stmt = (
            select(PackageBooking)
            .where(PackageBooking.customer_id == customer_id)
            .order_by(PackageBooking.id.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def get_by_package(self, package_id: int, skip: int = 0, limit: int = 50) -> Sequence[PackageBooking]:
        stmt = (
            select(PackageBooking)
            .where(PackageBooking.package_id == package_id)
            .order_by(PackageBooking.id.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def count_booked_for_date(self, package_id: int, travel_date: date) -> int:
        """Count total persons booked for a specific package on a specific date."""
        result = self.db.scalar(
            select(func.coalesce(func.sum(PackageBooking.num_persons), 0)).where(
                PackageBooking.package_id == package_id,
                PackageBooking.travel_date == travel_date,
                PackageBooking.status.in_([
                    PackageBookingStatus.PENDING,
                    PackageBookingStatus.CONFIRMED,
                ]),
            )
        )
        return int(result or 0)

    def get_active_bookings(self, skip: int = 0, limit: int = 100) -> Sequence[PackageBooking]:
        stmt = (
            select(PackageBooking)
            .where(PackageBooking.status.in_([
                PackageBookingStatus.PENDING,
                PackageBookingStatus.CONFIRMED,
            ]))
            .order_by(PackageBooking.id.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()
