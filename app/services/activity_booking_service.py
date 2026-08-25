from datetime import date
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError, ConflictError
from ..models.activity import Activity
from ..models.activity_booking import ActivityBooking, ActivityBookingStatus
from ..repositories.activity_booking_repository import ActivityBookingRepository
from ..repositories.activity_repository import ActivityRepository
from ..schemas.activity_booking import ActivityBookingCreate, ActivityBookingUpdate


class ActivityBookingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ActivityBookingRepository(db)
        self.act_repo = ActivityRepository(db)

    def _validate_booking(self, activity: Activity, payload: ActivityBookingCreate) -> None:
        """Validate all booking criteria before creating."""
        if not activity.is_active:
            raise ConflictError("This activity is currently not available for booking")

        if activity.available_dates:
            import json
            try:
                available = json.loads(activity.available_dates)
                if isinstance(available, list) and str(payload.booking_date) not in available:
                    raise ConflictError(
                        f"Date {payload.booking_date} is not available. "
                        f"Available dates: {', '.join(available[:10])}"
                    )
            except (json.JSONDecodeError, TypeError):
                pass

        if activity.min_age and payload.participant_age and payload.participant_age < activity.min_age:
            raise ConflictError(
                f"Minimum age for this activity is {activity.min_age} years"
            )

        booked = self.repo.count_booked_for_date(activity.activity_id, payload.booking_date)
        remaining = activity.max_participants - booked
        if remaining <= 0:
            raise ConflictError(
                f"Fully booked for {payload.booking_date}. No spots available."
            )
        if payload.num_persons > remaining:
            raise ConflictError(
                f"Only {remaining} spot(s) left for {payload.booking_date}, "
                f"but you requested {payload.num_persons}"
            )

        if not payload.contact_name or not payload.contact_email:
            raise ConflictError("Contact name and email are required for booking")

    def create(self, customer_id: int, payload: ActivityBookingCreate) -> ActivityBooking:
        """Create a new activity booking with full validation."""
        activity = self.act_repo.get_or_404(payload.activity_id)
        self._validate_booking(activity, payload)

        total = float(activity.price) * payload.num_persons

        booking_data = {
            "booking_ref": self.repo.generate_booking_ref(),
            "activity_id": payload.activity_id,
            "customer_id": customer_id,
            "booking_date": payload.booking_date,
            "num_persons": payload.num_persons,
            "total_amount": total,
            "status": ActivityBookingStatus.CONFIRMED,
            "special_requests": payload.special_requests,
            "dietary_requirements": payload.dietary_requirements,
            "contact_name": payload.contact_name,
            "contact_email": payload.contact_email,
            "contact_phone": payload.contact_phone,
            "emergency_contact": payload.emergency_contact,
            "participant_age": payload.participant_age,
            "health_conditions": payload.health_conditions,
            "pick_up_location": payload.pick_up_location,
            "pick_up_time": payload.pick_up_time,
        }
        booking = self.repo.create(booking_data)

        activity.booked_count = (activity.booked_count or 0) + payload.num_persons
        self.db.commit()
        self.db.refresh(activity)

        return booking

    def get(self, booking_id: int) -> ActivityBooking:
        return self.repo.get_or_404(booking_id)

    def get_customer_bookings(self, customer_id: int, skip=0, limit=50):
        return self.repo.get_by_customer(customer_id, skip=skip, limit=limit)

    def cancel(self, booking_id: int, customer_id: int) -> ActivityBooking:
        booking = self.repo.get_or_404(booking_id)
        if booking.customer_id != customer_id:
            raise ConflictError("You can only cancel your own bookings")
        if booking.status in (ActivityBookingStatus.CANCELLED, ActivityBookingStatus.COMPLETED):
            raise ConflictError(f"Cannot cancel a {booking.status.value} booking")

        booking.status = ActivityBookingStatus.CANCELLED

        activity = self.act_repo.get(booking.activity_id)
        if activity:
            activity.booked_count = max(0, (activity.booked_count or 0) - booking.num_persons)

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update_status(self, booking_id: int, payload: ActivityBookingUpdate) -> ActivityBooking:
        booking = self.repo.get_or_404(booking_id)
        if payload.status:
            booking.status = payload.status
        if payload.special_requests is not None:
            booking.special_requests = payload.special_requests
        if payload.contact_phone is not None:
            booking.contact_phone = payload.contact_phone
        if payload.emergency_contact is not None:
            booking.emergency_contact = payload.emergency_contact
        if payload.pick_up_location is not None:
            booking.pick_up_location = payload.pick_up_location
        if payload.pick_up_time is not None:
            booking.pick_up_time = payload.pick_up_time
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_available_spots(self, activity_id: int, booking_date: date) -> dict:
        activity = self.act_repo.get_or_404(activity_id)
        booked = self.repo.count_booked_for_date(activity_id, booking_date)
        max_p = activity.max_participants or 20
        remaining = max(0, max_p - booked)
        return {
            "activity_id": activity_id,
            "booking_date": str(booking_date),
            "max_participants": max_p,
            "booked_spots": booked,
            "available_spots": remaining,
            "is_available": remaining > 0,
        }
