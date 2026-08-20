from datetime import date
from sqlalchemy.orm import Session

from ..core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from ..models import BookingStatus
from ..repositories import (
    BookingRepository, CustomerRepository,
    HotelRepository, GuideRepository,
)
from ..schemas.booking import BookingCreate, BookingUpdate, BookingStatusUpdate


class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BookingRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.hotel_repo = HotelRepository(db)
        self.guide_repo = GuideRepository(db)

    def get(self, booking_id: int):
        return self.repo.get_or_404(booking_id)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(skip=skip, limit=limit)

    def list_by_customer(self, customer_id: int, skip: int = 0, limit: int = 100):
        return self.repo.list_by_customer(customer_id, skip=skip, limit=limit)

    def list_by_hotel(self, hotel_id: int, skip: int = 0, limit: int = 100):
        return self.repo.list_by_hotel(hotel_id, skip=skip, limit=limit)

    def list_by_status(self, status: BookingStatus, skip: int = 0, limit: int = 100):
        return self.repo.list_by_status(status, skip=skip, limit=limit)

    def create(self, payload: BookingCreate):
        if not self.customer_repo.exists(payload.customer_id):
            raise ConflictError("Customer does not exist", detail=f"customer_id={payload.customer_id}")
        if not self.hotel_repo.exists(payload.hotel_id):
            raise ConflictError("Hotel does not exist", detail=f"hotel_id={payload.hotel_id}")
        if payload.guide_id and not self.guide_repo.exists(payload.guide_id):
            raise ConflictError("Guide does not exist", detail=f"guide_id={payload.guide_id}")
        
        if self.repo.has_overlapping(
            hotel_id=payload.hotel_id,
            check_in=payload.check_in_date,
            check_out=payload.check_out_date,
        ):
            raise BusinessRuleError(
                "Hotel is not available for the selected dates",
                detail=f"hotel_id={payload.hotel_id}, dates={payload.check_in_date}→{payload.check_out_date}",
            )
        return self.repo.create(payload.model_dump())

    def update(self, booking_id: int, payload: BookingUpdate):
        booking = self.repo.get_or_404(booking_id)

        if booking.booking_status in (BookingStatus.COMPLETED, BookingStatus.CANCELLED):
            raise BusinessRuleError(
                f"Cannot modify a {booking.booking_status.value} booking",
                detail=f"booking_id={booking_id}",
            )

        new_check_in = payload.check_in_date or booking.check_in_date
        new_check_out = payload.check_out_date or booking.check_out_date
        new_hotel_id = payload.hotel_id or booking.hotel_id

        if (payload.check_in_date or payload.check_out_date or payload.hotel_id):
            if self.repo.has_overlapping(
                hotel_id=new_hotel_id,
                check_in=new_check_in,
                check_out=new_check_out,
                exclude_id=booking_id,
            ):
                raise BusinessRuleError(
                    "Hotel is not available for the new dates",
                    detail=f"hotel_id={new_hotel_id}",
                )

        return self.repo.update(booking_id, payload.model_dump(exclude_unset=True))


    _VALID_TRANSITIONS = {
        BookingStatus.PENDING:    {BookingStatus.CONFIRMED, BookingStatus.CANCELLED},
        BookingStatus.CONFIRMED:  {BookingStatus.COMPLETED, BookingStatus.CANCELLED},
        BookingStatus.CANCELLED:  set(),
        BookingStatus.COMPLETED:  set(),
    }

    def change_status(self, booking_id: int, new_status: BookingStatus):
        """Centralised status transition validator."""
        booking = self.repo.get_or_404(booking_id)
        current = booking.booking_status

        if current == new_status:
            return booking  

        allowed = self._VALID_TRANSITIONS.get(current, set())
        if new_status not in allowed:
            raise BusinessRuleError(
                f"Cannot transition booking from {current.value} to {new_status.value}",
                detail=f"booking_id={booking_id}",
            )

        return self.repo.update(booking_id, {"booking_status": new_status})

    def confirm(self, booking_id: int):
        return self.change_status(booking_id, BookingStatus.CONFIRMED)

    def cancel(self, booking_id: int):
        return self.change_status(booking_id, BookingStatus.CANCELLED)

    def complete(self, booking_id: int):
        return self.change_status(booking_id, BookingStatus.COMPLETED)

    def delete(self, booking_id: int) -> None:
        booking = self.repo.get_or_404(booking_id)
        if booking.booking_status != BookingStatus.PENDING:
            raise BusinessRuleError(
                f"Cannot delete a {booking.booking_status.value} booking — cancel instead",
                detail=f"booking_id={booking_id}",
            )
        self.repo.delete(booking_id)