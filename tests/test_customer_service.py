import pytest
from sqlalchemy.orm import Session

from app.services.customer_service import CustomerService
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.core.exceptions import NotFoundError, ConflictError


class TestCustomerServiceGet:
    def test_get_existing(self, db_session: Session, sample_customer):
        svc = CustomerService(db_session)
        cust = svc.get(sample_customer.customer_id)
        assert cust.customer_name == sample_customer.customer_name

    def test_get_nonexistent(self, db_session: Session):
        svc = CustomerService(db_session)
        with pytest.raises(NotFoundError):
            svc.get(999999)


class TestCustomerServiceList:
    def test_list(self, db_session: Session, sample_customer):
        svc = CustomerService(db_session)
        custs = svc.list()
        assert len(custs) >= 1

    def test_list_empty(self, db_session: Session):
        svc = CustomerService(db_session)
        assert svc.list() == []

    def test_list_pagination(self, db_session: Session):
        svc = CustomerService(db_session)
        for i in range(5):
            svc.create(CustomerCreate(
                customer_name=f"Cust {i}",
                customer_email=f"cust{i}@test.com",
                customer_password="Test12345",
            ))
        page = svc.list(skip=0, limit=2)
        assert len(page) == 2


class TestCustomerServiceCreate:
    def test_create(self, db_session: Session):
        svc = CustomerService(db_session)
        cust = svc.create(CustomerCreate(
            customer_name="New Person",
            customer_email="new@test.com",
            customer_password="Secure123",
        ))
        assert cust.customer_id is not None
        assert cust.customer_password != "Secure123"  

    def test_create_duplicate_email(self, db_session: Session, sample_customer):
        svc = CustomerService(db_session)
        with pytest.raises(ConflictError, match="already registered"):
            svc.create(CustomerCreate(
                customer_name="Dup",
                customer_email=sample_customer.customer_email,
                customer_password="Secure123",
            ))


class TestCustomerServiceUpdate:
    def test_update_name(self, db_session: Session, sample_customer):
        svc = CustomerService(db_session)
        updated = svc.update(sample_customer.customer_id, CustomerUpdate(
            customer_name="Updated Name",
        ))
        assert updated.customer_name == "Updated Name"

    def test_update_password(self, db_session: Session, sample_customer):
        svc = CustomerService(db_session)
        svc.update(sample_customer.customer_id, CustomerUpdate(
            customer_password="NewPass123",
        ))
        from app.core.security import verify_password
        cust = svc.get(sample_customer.customer_id)
        assert verify_password("NewPass123", cust.customer_password)

    def test_update_nonexistent_raises(self, db_session: Session):
        svc = CustomerService(db_session)
        with pytest.raises(NotFoundError):
            svc.update(999999, CustomerUpdate(customer_name="X"))


class TestCustomerServiceDelete:
    def test_delete(self, db_session: Session, sample_customer):
        svc = CustomerService(db_session)
        svc.delete(sample_customer.customer_id)
        with pytest.raises(NotFoundError):
            svc.get(sample_customer.customer_id)

    def test_delete_nonexistent_raises(self, db_session: Session):
        svc = CustomerService(db_session)
        with pytest.raises(NotFoundError):
            svc.delete(999999)
