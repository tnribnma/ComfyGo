import pytest
from datetime import date, timedelta
from pydantic import ValidationError

from app.schemas.hotel import HotelCreate, HotelUpdate, HotelOut, DestinationOut
from app.schemas.booking import BookingCreate, BookingUpdate, BookingStatusUpdate
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerLogin
from app.schemas.admin import AdminCreate, AdminUpdate, AdminLogin
from app.schemas.auth import TokenResponse, RefreshTokenRequest
from app.models.booking import BookingStatus


class TestHotelCreateSchema:
    def test_valid_hotel(self):
        h = HotelCreate(
            hotel_name="Grand Palace",
            hotel_address="123 Sukhumvit Rd",
            hotel_city="Bangkok",
            hotel_country="Thailand",
        )
        assert h.hotel_name == "Grand Palace"
        assert h.breakfast_included is False
        assert h.has_pool is False

    def test_all_optional_fields(self):
        h = HotelCreate(
            hotel_name="Test",
            hotel_address="123 Main St",
            hotel_city="NYC",
            hotel_country="USA",
            hotel_phone="5551234",
            hotel_email="test@hotel.com",
            hotel_description="Nice place",
            hotel_rating=4.5,
            price_per_night=200.0,
            breakfast_included=True,
            has_pool=True,
            has_wifi=True,
            has_parking=True,
            free_cancellation=True,
        )
        assert h.hotel_rating == 4.5
        assert h.price_per_night == 200.0

    def test_name_too_short(self):
        with pytest.raises(ValidationError):
            HotelCreate(
                hotel_name="A",
                hotel_address="123 Main St",
                hotel_city="NYC",
                hotel_country="USA",
            )

    def test_name_too_long(self):
        with pytest.raises(ValidationError):
            HotelCreate(
                hotel_name="A" * 151,
                hotel_address="123 Main St",
                hotel_city="NYC",
                hotel_country="USA",
            )

    def test_rating_out_of_range(self):
        with pytest.raises(ValidationError):
            HotelCreate(
                hotel_name="Test Hotel",
                hotel_address="123 Main St",
                hotel_city="NYC",
                hotel_country="USA",
                hotel_rating=6.0,
            )

    def test_negative_price(self):
        with pytest.raises(ValidationError):
            HotelCreate(
                hotel_name="Test Hotel",
                hotel_address="123 Main St",
                hotel_city="NYC",
                hotel_country="USA",
                price_per_night=-10.0,
            )

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            HotelCreate(
                hotel_name="Test Hotel",
                hotel_address="123 Main St",
                hotel_city="NYC",
                hotel_country="USA",
                hotel_email="not-an-email",
            )


class TestHotelUpdateSchema:
    def test_partial_update(self):
        h = HotelUpdate(hotel_name="New Name")
        assert h.hotel_name == "New Name"
        assert h.hotel_address is None  

    def test_empty_update_valid(self):
        h = HotelUpdate()
        assert h.model_dump(exclude_unset=True) == {}


class TestBookingCreateSchema:
    def test_valid_booking(self):
        b = BookingCreate(
            customer_id=1,
            hotel_id=1,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3),
            total_amount=300.0,
        )
        assert b.number_of_guests == 1
        assert b.booking_status == BookingStatus.PENDING

    def test_check_out_before_check_in_invalid(self):
        with pytest.raises(ValidationError):
            BookingCreate(
                customer_id=1,
                hotel_id=1,
                check_in_date=date.today() + timedelta(days=5),
                check_out_date=date.today() + timedelta(days=2),
                total_amount=100.0,
            )

    def test_check_out_equals_check_in_invalid(self):
        with pytest.raises(ValidationError):
            BookingCreate(
                customer_id=1,
                hotel_id=1,
                check_in_date=date(2026, 1, 1),
                check_out_date=date(2026, 1, 1),
                total_amount=100.0,
            )

    def test_negative_guests_invalid(self):
        with pytest.raises(ValidationError):
            BookingCreate(
                customer_id=1,
                hotel_id=1,
                check_in_date=date(2026, 1, 1),
                check_out_date=date(2026, 1, 2),
                number_of_guests=0,
                total_amount=100.0,
            )

    def test_too_many_guests(self):
        with pytest.raises(ValidationError):
            BookingCreate(
                customer_id=1,
                hotel_id=1,
                check_in_date=date(2026, 1, 1),
                check_out_date=date(2026, 1, 2),
                number_of_guests=21,
                total_amount=100.0,
            )

    def test_zero_total_invalid(self):
        with pytest.raises(ValidationError):
            BookingCreate(
                customer_id=1,
                hotel_id=1,
                check_in_date=date(2026, 1, 1),
                check_out_date=date(2026, 1, 2),
                total_amount=0,
            )

    def test_negative_customer_id_invalid(self):
        with pytest.raises(ValidationError):
            BookingCreate(
                customer_id=-1,
                hotel_id=1,
                check_in_date=date(2026, 1, 1),
                check_out_date=date(2026, 1, 2),
                total_amount=100.0,
            )


class TestBookingUpdateSchema:
    def test_partial_update(self):
        b = BookingUpdate(check_in_date=date(2026, 6, 1))
        assert b.check_in_date == date(2026, 6, 1)
        assert b.check_out_date is None

    def test_invalid_date_range_update(self):
        with pytest.raises(ValidationError):
            BookingUpdate(
                check_in_date=date(2026, 6, 10),
                check_out_date=date(2026, 6, 1),
            )


class TestBookingStatusUpdateSchema:
    def test_valid_status(self):
        s = BookingStatusUpdate(booking_status=BookingStatus.CONFIRMED)
        assert s.booking_status == BookingStatus.CONFIRMED


class TestCustomerCreateSchema:
    def test_valid_customer(self):
        c = CustomerCreate(
            customer_name="John Doe",
            customer_email="john@test.com",
            customer_password="Secure123",
        )
        assert c.customer_name == "John Doe"

    def test_weak_password_no_uppercase(self):
        with pytest.raises(ValidationError):
            CustomerCreate(
                customer_name="John",
                customer_email="j@test.com",
                customer_password="nouppercase1",
            )

    def test_weak_password_no_digit(self):
        with pytest.raises(ValidationError):
            CustomerCreate(
                customer_name="John",
                customer_email="j@test.com",
                customer_password="NoDigitHere",
            )

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            CustomerCreate(
                customer_name="John",
                customer_email="j@test.com",
                customer_password="Ab1",
            )

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            CustomerCreate(
                customer_name="John",
                customer_email="not-email",
                customer_password="Secure123",
            )

    def test_name_too_short(self):
        with pytest.raises(ValidationError):
            CustomerCreate(
                customer_name="J",
                customer_email="j@test.com",
                customer_password="Secure123",
            )


class TestCustomerUpdateSchema:
    def test_partial_update(self):
        c = CustomerUpdate(customer_name="New Name")
        assert c.customer_name == "New Name"
        assert c.customer_email is None


class TestAdminCreateSchema:
    def test_valid_admin(self):
        a = AdminCreate(
            admin_name="Super Admin",
            admin_email="admin@test.com",
            admin_password="Admin1234",
        )
        assert a.admin_name == "Super Admin"

    def test_weak_password(self):
        with pytest.raises(ValidationError):
            AdminCreate(
                admin_name="Admin",
                admin_email="a@test.com",
                admin_password="weak",
            )


class TestAdminLoginSchema:
    def test_valid_login(self):
        l = AdminLogin(admin_email="admin@test.com", admin_password="pass")
        assert l.admin_email == "admin@test.com"


class TestTokenResponse:
    def test_token_response(self):
        t = TokenResponse(
            access_token="abc",
            refresh_token="xyz",
            role="admin",
            user_id=1,
        )
        assert t.token_type == "bearer"


class TestRefreshTokenRequest:
    def test_refresh_request(self):
        r = RefreshTokenRequest(refresh_token="my_token")
        assert r.refresh_token == "my_token"


class TestDestinationOut:
    def test_valid(self):
        d = DestinationOut(city="Bangkok", country="Thailand", hotel_count=5)
        assert d.city == "Bangkok"
        assert d.hotel_count == 5
