import pytest
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.services.booking_service import BookingService
from app.schemas.booking import BookingCreate, BookingUpdate
from app.models.booking import BookingStatus
from app.core.exceptions import ConflictError, BusinessRuleError, NotFoundError


class TestBookingServiceCreate:
    def test_create_booking(self, db_session: Session, sample_customer, sample_hotel):
        svc = BookingService(db_session)
        payload = BookingCreate(
            customer_id=sample_customer.customer_id,
            hotel_id=sample_hotel.hotel_id,
            check_in_date=date.today() + timedelta(days=7),
            check_out_date=date.today() + timedelta(days=10),
            total_amount=360.0,
        )
        booking = svc.create(payload)
        assert booking.booking_id is not None
        assert booking.booking_status == BookingStatus.PENDING
        assert booking.total_amount == 360.0

    def test_create_booking_sets_today_date(self, db_session: Session, sample_customer, sample_hotel):
        svc = BookingService(db_session)
        payload = BookingCreate(
            customer_id=sample_customer.customer_id,
            hotel_id=sample_hotel.hotel_id,
            check_in_date=date.today() + timedelta(days=7),
            check_out_date=date.today() + timedelta(days=10),
            total_amount=360.0,
        )
        booking = svc.create(payload)
        assert booking.booking_date == date.today()

    def test_create_booking_invalid_customer(self, db_session: Session, sample_hotel):
        svc = BookingService(db_session)
        payload = BookingCreate(
            customer_id=999999,
            hotel_id=sample_hotel.hotel_id,
            check_in_date=date.today() + timedelta(days=7),
            check_out_date=date.today() + timedelta(days=10),
            total_amount=360.0,
        )
        with pytest.raises(ConflictError, match="Customer does not exist"):
            svc.create(payload)

    def test_create_booking_invalid_hotel(self, db_session: Session, sample_customer):
        svc = BookingService(db_session)
        payload = BookingCreate(
            customer_id=sample_customer.customer_id,
            hotel_id=999999,
            check_in_date=date.today() + timedelta(days=7),
            check_out_date=date.today() + timedelta(days=10),
            total_amount=360.0,
        )
        with pytest.raises(ConflictError, match="Hotel does not exist"):
            svc.create(payload)

    def test_create_booking_invalid_guide(self, db_session: Session, sample_customer, sample_hotel):
        svc = BookingService(db_session)
        payload = BookingCreate(
            customer_id=sample_customer.customer_id,
            hotel_id=sample_hotel.hotel_id,
            guide_id=999999,
            check_in_date=date.today() + timedelta(days=7),
            check_out_date=date.today() + timedelta(days=10),
            total_amount=360.0,
        )
        with pytest.raises(ConflictError, match="Guide does not exist"):
            svc.create(payload)

    def test_create_booking_overlapping_dates(self, db_session: Session, sample_customer, sample_hotel):
        svc = BookingService(db_session)
        ci1 = date.today() + timedelta(days=7)
        co1 = date.today() + timedelta(days=12)

        svc.create(BookingCreate(
            customer_id=sample_customer.customer_id,
            hotel_id=sample_hotel.hotel_id,
            check_in_date=ci1,
            check_out_date=co1,
            total_amount=500.0,
        ))

        with pytest.raises(BusinessRuleError, match="not available"):
            svc.create(BookingCreate(
                customer_id=sample_customer.customer_id,
                hotel_id=sample_hotel.hotel_id,
                check_in_date=ci1 + timedelta(days=2),
                check_out_date=co1 + timedelta(days=2),
                total_amount=400.0,
            ))


class TestBookingServiceGet:
    def test_get_existing(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        b = svc.get(sample_booking.booking_id)
        assert b.booking_id == sample_booking.booking_id

    def test_get_nonexistent(self, db_session: Session):
        svc = BookingService(db_session)
        with pytest.raises(NotFoundError):
            svc.get(999999)


class TestBookingServiceList:
    def test_list(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        bookings = svc.list()
        assert len(bookings) >= 1

    def test_list_by_customer(self, db_session: Session, sample_booking, sample_customer):
        svc = BookingService(db_session)
        bookings = svc.list_by_customer(sample_customer.customer_id)
        assert len(bookings) >= 1

    def test_list_by_hotel(self, db_session: Session, sample_booking, sample_hotel):
        svc = BookingService(db_session)
        bookings = svc.list_by_hotel(sample_hotel.hotel_id)
        assert len(bookings) >= 1

    def test_list_by_status(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        bookings = svc.list_by_status(BookingStatus.PENDING)
        assert len(bookings) >= 1


class TestBookingStatusTransitions:
    def test_pending_to_confirmed(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        confirmed = svc.confirm(sample_booking.booking_id)
        assert confirmed.booking_status == BookingStatus.CONFIRMED

    def test_pending_to_cancelled(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        cancelled = svc.cancel(sample_booking.booking_id)
        assert cancelled.booking_status == BookingStatus.CANCELLED

    def test_pending_to_completed_invalid(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        with pytest.raises(BusinessRuleError, match="Cannot transition"):
            svc.complete(sample_booking.booking_id)

    def test_confirmed_to_completed(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.confirm(sample_booking.booking_id)
        completed = svc.complete(sample_booking.booking_id)
        assert completed.booking_status == BookingStatus.COMPLETED

    def test_confirmed_to_cancelled(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.confirm(sample_booking.booking_id)
        cancelled = svc.cancel(sample_booking.booking_id)
        assert cancelled.booking_status == BookingStatus.CANCELLED

    def test_cancelled_to_any_invalid(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.cancel(sample_booking.booking_id)
        with pytest.raises(BusinessRuleError):
            svc.confirm(sample_booking.booking_id)

    def test_completed_to_any_invalid(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.confirm(sample_booking.booking_id)
        svc.complete(sample_booking.booking_id)
        with pytest.raises(BusinessRuleError):
            svc.cancel(sample_booking.booking_id)

    def test_same_status_noop(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        result = svc.change_status(sample_booking.booking_id, BookingStatus.PENDING)
        assert result.booking_status == BookingStatus.PENDING


class TestBookingServiceUpdate:
    def test_update_booking(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        new_check_in = date.today() + timedelta(days=14)
        new_check_out = date.today() + timedelta(days=17)
        updated = svc.update(sample_booking.booking_id, BookingUpdate(
            check_in_date=new_check_in,
            check_out_date=new_check_out,
            number_of_guests=3,
        ))
        assert updated.check_in_date == new_check_in
        assert updated.number_of_guests == 3

    def test_update_completed_booking_rejected(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.confirm(sample_booking.booking_id)
        svc.complete(sample_booking.booking_id)
        with pytest.raises(BusinessRuleError, match="Cannot modify"):
            svc.update(sample_booking.booking_id, BookingUpdate(number_of_guests=5))

    def test_update_cancelled_booking_rejected(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.cancel(sample_booking.booking_id)
        with pytest.raises(BusinessRuleError, match="Cannot modify"):
            svc.update(sample_booking.booking_id, BookingUpdate(number_of_guests=5))


class TestBookingServiceDelete:
    def test_delete_pending_booking(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.delete(sample_booking.booking_id)
        with pytest.raises(NotFoundError):
            svc.get(sample_booking.booking_id)

    def test_delete_confirmed_booking_rejected(self, db_session: Session, sample_booking):
        svc = BookingService(db_session)
        svc.confirm(sample_booking.booking_id)
        with pytest.raises(BusinessRuleError, match="cancel instead"):
            svc.delete(sample_booking.booking_id)

    def test_delete_nonexistent_raises(self, db_session: Session):
        svc = BookingService(db_session)
        with pytest.raises(NotFoundError):
            svc.delete(999999)
