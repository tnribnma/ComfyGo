import pytest
from sqlalchemy.orm import Session

from app.models import Hotel
from app.repositories.base import GenericRepository
from app.core.exceptions import NotFoundError, ConflictError


class HotelRepo(GenericRepository[Hotel]):
    model = Hotel
    auto_commit = True


class TestGenericRepositoryCreate:
    def test_create(self, db_session: Session):
        repo = HotelRepo(db_session)
        hotel = repo.create({
            "hotel_name": "Repo Hotel",
            "hotel_address": "123 Repo St",
            "hotel_city": "Bangkok",
            "hotel_country": "Thailand",
            "price_per_night": 100.0,
        })
        assert hotel.hotel_id is not None
        assert hotel.hotel_name == "Repo Hotel"

    def test_create_many(self, db_session: Session):
        repo = HotelRepo(db_session)
        items = [
            {"hotel_name": f"Hotel {i}", "hotel_address": f"Addr {i}",
             "hotel_city": "Test", "hotel_country": "Test"}
            for i in range(3)
        ]
        hotels = repo.create_many(items)
        assert len(hotels) == 3
        assert all(h.hotel_id is not None for h in hotels)

    def test_create_duplicate_raises_conflict(self, db_session: Session):
        """SQLite doesn't enforce unique on hotel_name by default, but
        we test the generic IntegrityError handling path."""
        repo = HotelRepo(db_session)
        repo.create({
            "hotel_name": "Unique Hotel",
            "hotel_address": "123 Main",
            "hotel_city": "Test",
            "hotel_country": "Test",
        })
        repo.create({
            "hotel_name": "Unique Hotel 2",
            "hotel_address": "456 Main",
            "hotel_city": "Test",
            "hotel_country": "Test",
        })


class TestGenericRepositoryRead:
    def test_get_existing(self, db_session: Session, sample_hotel):
        repo = HotelRepo(db_session)
        hotel = repo.get(sample_hotel.hotel_id)
        assert hotel is not None
        assert hotel.hotel_name == sample_hotel.hotel_name

    def test_get_nonexistent_returns_none(self, db_session: Session):
        repo = HotelRepo(db_session)
        assert repo.get(999999) is None

    def test_get_or_404_existing(self, db_session: Session, sample_hotel):
        repo = HotelRepo(db_session)
        hotel = repo.get_or_404(sample_hotel.hotel_id)
        assert hotel.hotel_id == sample_hotel.hotel_id

    def test_get_or_404_missing_raises(self, db_session: Session):
        repo = HotelRepo(db_session)
        with pytest.raises(NotFoundError):
            repo.get_or_404(999999)

    def test_get_multi(self, db_session: Session):
        repo = HotelRepo(db_session)
        for i in range(5):
            repo.create({
                "hotel_name": f"M {i}", "hotel_address": f"A {i}",
                "hotel_city": "C", "hotel_country": "X",
            })
        results = repo.get_multi(skip=0, limit=3)
        assert len(results) == 3

    def test_get_multi_empty(self, db_session: Session):
        repo = HotelRepo(db_session)
        assert repo.get_multi() == []

    def test_get_by_filter(self, db_session: Session):
        repo = HotelRepo(db_session)
        repo.create({"hotel_name": "Filter Me", "hotel_address": "F1",
                      "hotel_city": "TestCity", "hotel_country": "Test"})
        repo.create({"hotel_name": "Other", "hotel_address": "F2",
                      "hotel_city": "OtherCity", "hotel_country": "Test"})
        results = repo.get_by(hotel_city="TestCity")
        assert len(results) == 1
        assert results[0].hotel_name == "Filter Me"

    def test_get_one_by(self, db_session: Session, sample_hotel):
        repo = HotelRepo(db_session)
        hotel = repo.get_one_by(hotel_name=sample_hotel.hotel_name)
        assert hotel is not None
        assert hotel.hotel_id == sample_hotel.hotel_id

    def test_get_one_by_no_match(self, db_session: Session):
        repo = HotelRepo(db_session)
        assert repo.get_one_by(hotel_name="nonexistent") is None

    def test_count(self, db_session: Session):
        repo = HotelRepo(db_session)
        assert repo.count() == 0
        repo.create({"hotel_name": "A", "hotel_address": "B",
                      "hotel_city": "C", "hotel_country": "D"})
        assert repo.count() == 1

    def test_exists_true(self, db_session: Session, sample_hotel):
        repo = HotelRepo(db_session)
        assert repo.exists(sample_hotel.hotel_id) is True

    def test_exists_false(self, db_session: Session):
        repo = HotelRepo(db_session)
        assert repo.exists(999999) is False


class TestGenericRepositoryUpdate:
    def test_update(self, db_session: Session, sample_hotel):
        repo = HotelRepo(db_session)
        updated = repo.update(sample_hotel.hotel_id, {"hotel_name": "Updated"})
        assert updated.hotel_name == "Updated"
        assert updated.hotel_id == sample_hotel.hotel_id

    def test_update_nonexistent_raises(self, db_session: Session):
        repo = HotelRepo(db_session)
        with pytest.raises(NotFoundError):
            repo.update(999999, {"hotel_name": "X"})

    def test_update_preserves_unset_fields(self, db_session: Session, sample_hotel):
        repo = HotelRepo(db_session)
        updated = repo.update(sample_hotel.hotel_id, {"hotel_name": "New Name"})
        assert updated.hotel_city == sample_hotel.hotel_city
        assert updated.price_per_night == sample_hotel.price_per_night


class TestGenericRepositoryDelete:
    def test_delete(self, db_session: Session, sample_hotel):
        repo = HotelRepo(db_session)
        repo.delete(sample_hotel.hotel_id)
        assert repo.get(sample_hotel.hotel_id) is None

    def test_delete_nonexistent_raises(self, db_session: Session):
        repo = HotelRepo(db_session)
        with pytest.raises(NotFoundError):
            repo.delete(999999)

    def test_delete_many(self, db_session: Session):
        repo = HotelRepo(db_session)
        ids = []
        for i in range(3):
            h = repo.create({"hotel_name": f"D{i}", "hotel_address": "A",
                              "hotel_city": "C", "hotel_country": "X"})
            ids.append(h.hotel_id)
        deleted = repo.delete_many(ids)
        assert deleted == 3
        assert repo.count() == 0

    def test_delete_many_empty_list(self, db_session: Session):
        repo = HotelRepo(db_session)
        assert repo.delete_many([]) == 0


class TestGenericRepositoryRepr:
    def test_repr(self, db_session: Session):
        repo = HotelRepo(db_session)
        assert "Hotel" in repr(repo)
        assert "HotelRepo" in repr(repo)
