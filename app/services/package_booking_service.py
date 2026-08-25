from datetime import date
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError, ConflictError
from ..models.package import TourPackage
from ..models.package_booking import PackageBooking, PackageBookingStatus
from ..repositories.package_booking_repository import PackageBookingRepository
from ..repositories.package_repository import TourPackageRepository
from ..schemas.package_booking import PackageBookingCreate, PackageBookingUpdate


class PackageBookingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PackageBookingRepository(db)
        self.pkg_repo = TourPackageRepository(db)

    def _validate_booking(self, package: TourPackage, payload: PackageBookingCreate) -> None:
        """Validate all booking criteria before creating."""
        if not package.is_active:
            raise ConflictError("This package is currently not available for booking")

        if package.available_dates:
            import json
            try:
                available = json.loads(package.available_dates)
                if isinstance(available, list) and str(payload.travel_date) not in available:
                    raise ConflictError(
                        f"Date {payload.travel_date} is not available. "
                        f"Available dates: {', '.join(available[:10])}"
                    )
            except (json.JSONDecodeError, TypeError):
                pass 

        if payload.num_persons < package.group_size_min:
            raise ConflictError(
                f"Minimum {package.group_size_min} persons required for this package"
            )
        if payload.num_persons > package.group_size_max:
            raise ConflictError(
                f"Maximum {package.group_size_max} persons allowed for this package"
            )

        booked = self.repo.count_booked_for_date(package.package_id, payload.travel_date)
        remaining = package.max_group_size - booked
        if remaining <= 0:
            raise ConflictError(
                f"Fully booked for {payload.travel_date}. No seats available."
            )
        if payload.num_persons > remaining:
            raise ConflictError(
                f"Only {remaining} seat(s) left for {payload.travel_date}, "
                f"but you requested {payload.num_persons}"
            )

        if not payload.contact_name or not payload.contact_email:
            raise ConflictError("Contact name and email are required for booking")

    def create(self, customer_id: int, payload: PackageBookingCreate) -> PackageBooking:
        """Create a new package booking with full validation."""
        package = self.pkg_repo.get_or_404(payload.package_id)

        self._validate_booking(package, payload)

        total = float(package.price_per_person) * payload.num_persons

        booking_data = {
            "booking_ref": self.repo.generate_booking_ref(),
            "package_id": payload.package_id,
            "customer_id": customer_id,
            "travel_date": payload.travel_date,
            "num_persons": payload.num_persons,
            "total_amount": total,
            "status": PackageBookingStatus.CONFIRMED,
            "special_requests": payload.special_requests,
            "dietary_requirements": payload.dietary_requirements,
            "contact_name": payload.contact_name,
            "contact_email": payload.contact_email,
            "contact_phone": payload.contact_phone,
            "emergency_contact": payload.emergency_contact,
        }
        booking = self.repo.create(booking_data)

        package.booked_count = (package.booked_count or 0) + payload.num_persons
        self.db.commit()
        self.db.refresh(package)

        return booking

    def get(self, booking_id: int) -> PackageBooking:
        return self.repo.get_or_404(booking_id)

    def get_by_ref(self, booking_ref: str) -> PackageBooking:
        booking = self.repo.get_one_by(booking_ref=booking_ref)
        if not booking:
            raise NotFoundError("Booking not found", detail=f"ref={booking_ref}")
        return booking

    def get_customer_bookings(self, customer_id: int, skip=0, limit=50):
        return self.repo.get_by_customer(customer_id, skip=skip, limit=limit)

    def cancel(self, booking_id: int, customer_id: int) -> PackageBooking:
        """Cancel a booking and release seats."""
        booking = self.repo.get_or_404(booking_id)
        if booking.customer_id != customer_id:
            raise ConflictError("You can only cancel your own bookings")
        if booking.status in (PackageBookingStatus.CANCELLED, PackageBookingStatus.COMPLETED):
            raise ConflictError(f"Cannot cancel a {booking.status.value} booking")

        booking.status = PackageBookingStatus.CANCELLED

        package = self.pkg_repo.get(booking.package_id)
        if package:
            package.booked_count = max(0, (package.booked_count or 0) - booking.num_persons)

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update_status(self, booking_id: int, payload: PackageBookingUpdate) -> PackageBooking:
        booking = self.repo.get_or_404(booking_id)
        if payload.status:
            booking.status = payload.status
        if payload.special_requests is not None:
            booking.special_requests = payload.special_requests
        if payload.dietary_requirements is not None:
            booking.dietary_requirements = payload.dietary_requirements
        if payload.contact_phone is not None:
            booking.contact_phone = payload.contact_phone
        if payload.emergency_contact is not None:
            booking.emergency_contact = payload.emergency_contact
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_available_seats(self, package_id: int, travel_date: date) -> dict:
        """Check available seats for a package on a specific date."""
        package = self.pkg_repo.get_or_404(package_id)
        booked = self.repo.count_booked_for_date(package_id, travel_date)
        max_seats = package.max_group_size or package.group_size_max or 15
        remaining = max(0, max_seats - booked)
        return {
            "package_id": package_id,
            "travel_date": str(travel_date),
            "max_seats": max_seats,
            "booked_seats": booked,
            "available_seats": remaining,
            "is_available": remaining > 0,
        }
