import pytest
from sqlalchemy.orm import Session

from app.services.hotel_service import HotelService
from app.schemas.hotel import HotelCreate, HotelUpdate
from app.core.exceptions import NotFoundError


class TestHotelServiceGet:
    def test_get_existing(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        hotel = svc.get(sample_hotel.hotel_id)
        assert hotel.hotel_name == sample_hotel.hotel_name

    def test_get_nonexistent_raises(self, db_session: Session):
        svc = HotelService(db_session)
        with pytest.raises(NotFoundError):
            svc.get(999999)


class TestHotelServiceList:
    def test_list_returns_hotels(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        hotels = svc.list()
        assert len(hotels) >= 1

    def test_list_empty(self, db_session: Session):
        svc = HotelService(db_session)
        hotels = svc.list()
        assert len(hotels) == 0

    def test_list_with_pagination(self, db_session: Session):
        svc = HotelService(db_session)
        for i in range(5):
            svc.create(HotelCreate(
                hotel_name=f"Hotel {i}",
                hotel_address=f"123 Street {i}",
                hotel_city="Bangkok",
                hotel_country="Thailand",
            ))
        page1 = svc.list(skip=0, limit=2)
        page2 = svc.list(skip=2, limit=2)
        assert len(page1) == 2
        assert len(page2) == 2
        assert page1[0].hotel_id != page2[0].hotel_id


class TestHotelServiceCreate:
    def test_create(self, db_session: Session):
        svc = HotelService(db_session)
        hotel = svc.create(HotelCreate(
            hotel_name="New Hotel",
            hotel_address="789 New St",
            hotel_city="Chiang Mai",
            hotel_country="Thailand",
            price_per_night=85.0,
            has_wifi=True,
        ))
        assert hotel.hotel_id is not None
        assert hotel.hotel_name == "New Hotel"
        assert hotel.price_per_night == 85.0
        assert hotel.has_wifi is True


class TestHotelServiceUpdate:
    def test_update(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        updated = svc.update(sample_hotel.hotel_id, HotelUpdate(
            hotel_name="Renamed Hotel",
            price_per_night=200.0,
        ))
        assert updated.hotel_name == "Renamed Hotel"
        assert updated.price_per_night == 200.0
        assert updated.hotel_city == sample_hotel.hotel_city

    def test_update_nonexistent_raises(self, db_session: Session):
        svc = HotelService(db_session)
        with pytest.raises(NotFoundError):
            svc.update(999999, HotelUpdate(hotel_name="X"))


class TestHotelServiceDelete:
    def test_delete(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        svc.delete(sample_hotel.hotel_id)
        with pytest.raises(NotFoundError):
            svc.get(sample_hotel.hotel_id)

    def test_delete_nonexistent_raises(self, db_session: Session):
        svc = HotelService(db_session)
        with pytest.raises(NotFoundError):
            svc.delete(999999)


class TestHotelServiceSearch:
    def test_search_by_city(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        results = svc.search(city="Bangkok")
        assert len(results) >= 1
        assert all(h.hotel_city == "Bangkok" for h in results)

    def test_search_no_results(self, db_session: Session):
        svc = HotelService(db_session)
        results = svc.search(city="NonExistent")
        assert len(results) == 0

    def test_search_by_price_range(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        results = svc.search(min_price=50, max_price=200)
        assert len(results) >= 1

    def test_search_by_amenities(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        results = svc.search(has_wifi=True)
        assert len(results) >= 1
        assert all(h.has_wifi for h in results)


class TestHotelServiceDestinations:
    def test_list_destinations(self, db_session: Session, sample_hotel):
        svc = HotelService(db_session)
        dests = svc.list_destinations()
        assert len(dests) >= 1
        assert dests[0]["city"] == "Bangkok"
        assert dests[0]["country"] == "Thailand"

    def test_list_destinations_empty(self, db_session: Session):
        svc = HotelService(db_session)
        dests = svc.list_destinations()
        assert len(dests) == 0
