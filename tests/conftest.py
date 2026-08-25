import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.models.base import Base
from app.database import Database, get_db
from app.main import app
from app.models import (
    Admin, Customer, Hotel, Guide, Employee,
    Booking, BookingStatus, Payment, PaymentMethod, PaymentStatus,
)
from app.core.security import get_password_hash


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    @event.listens_for(eng, "connect")
    def _set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


@pytest.fixture()
def db_session(engine) -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection, expire_on_commit=False)
    session = SessionLocal()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(engine) -> TestClient:
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection, expire_on_commit=False)

    def override_get_db():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def sample_admin(db_session: Session) -> Admin:
    admin = Admin(
        admin_name="Test Admin",
        admin_email="admin@test.com",
        admin_password=get_password_hash("Admin1234"),
        admin_phone="1234567890",
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture()
def sample_customer(db_session: Session) -> Customer:
    cust = Customer(
        customer_name="Test Customer",
        customer_email="customer@test.com",
        customer_phone="0987654321",
        customer_password=get_password_hash("Cust12345"),
        customer_address="123 Test St",
    )
    db_session.add(cust)
    db_session.commit()
    db_session.refresh(cust)
    return cust


@pytest.fixture()
def sample_hotel(db_session: Session) -> Hotel:
    hotel = Hotel(
        hotel_name="Test Hotel",
        hotel_address="456 Hotel Ave",
        hotel_city="Bangkok",
        hotel_country="Thailand",
        hotel_phone="5551234",
        hotel_email="hotel@test.com",
        hotel_description="A nice test hotel",
        hotel_rating=4.5,
        price_per_night=120.00,
        breakfast_included=True,
        has_wifi=True,
        has_pool=False,
        has_parking=True,
        free_cancellation=True,
    )
    db_session.add(hotel)
    db_session.commit()
    db_session.refresh(hotel)
    return hotel


@pytest.fixture()
def sample_guide(db_session: Session) -> Guide:
    guide = Guide(
        guide_name="Test Guide",
        guide_email="guide@test.com",
        guide_phone="1112223333",
        guide_city="Bangkok",
        guide_language="English",
        guide_experience=5,
        bio="Experienced test guide",
        specialties="Culture,Food",
        regions="Bangkok,Chiang Mai",
        hourly_rate=25.00,
        daily_rate=150.00,
        is_available=True,
    )
    db_session.add(guide)
    db_session.commit()
    db_session.refresh(guide)
    return guide


@pytest.fixture()
def sample_booking(db_session: Session, sample_customer, sample_hotel) -> Booking:
    booking = Booking(
        booking_date=date.today(),
        check_in_date=date.today() + timedelta(days=7),
        check_out_date=date.today() + timedelta(days=10),
        number_of_guests=2,
        booking_status=BookingStatus.PENDING,
        total_amount=360.00,
        customer_id=sample_customer.customer_id,
        hotel_id=sample_hotel.hotel_id,
    )
    db_session.add(booking)
    db_session.commit()
    db_session.refresh(booking)
    return booking
