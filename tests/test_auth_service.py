import pytest
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.core.security import decode_token, get_password_hash
from app.core.exceptions import AuthenticationError, ConflictError
from app.schemas.admin import AdminCreate, AdminLogin
from app.schemas.employee import EmployeeCreate, EmployeeLogin
from app.schemas.customer import CustomerCreate, CustomerLogin


class TestAdminRegistration:
    def test_register_admin_success(self, db_session: Session, sample_hotel):
        svc = AuthService(db_session)
        payload = AdminCreate(
            admin_name="New Admin",
            admin_email="newadmin@test.com",
            admin_password="Admin1234",
            admin_phone="1234567890",
        )
        admin = svc.register_admin(payload)
        assert admin.admin_id is not None
        assert admin.admin_email == "newadmin@test.com"
        assert admin.admin_password != "Admin1234"

    def test_register_duplicate_email(self, db_session: Session, sample_admin):
        svc = AuthService(db_session)
        payload = AdminCreate(
            admin_name="Dup Admin",
            admin_email=sample_admin.admin_email,
            admin_password="Admin1234",
        )
        with pytest.raises(ConflictError, match="already registered"):
            svc.register_admin(payload)


class TestAdminLogin:
    def test_login_admin_success(self, db_session: Session, sample_admin):
        svc = AuthService(db_session)
        payload = AdminLogin(
            admin_email=sample_admin.admin_email,
            admin_password="Admin1234",
        )
        tokens = svc.login_admin(payload)
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.role == "admin"
        assert tokens.user_id == sample_admin.admin_id

    def test_login_wrong_password(self, db_session: Session, sample_admin):
        svc = AuthService(db_session)
        payload = AdminLogin(
            admin_email=sample_admin.admin_email,
            admin_password="WrongPass1",
        )
        with pytest.raises(AuthenticationError):
            svc.login_admin(payload)

    def test_login_nonexistent_email(self, db_session: Session):
        svc = AuthService(db_session)
        payload = AdminLogin(
            admin_email="nobody@test.com",
            admin_password="Admin1234",
        )
        with pytest.raises(AuthenticationError):
            svc.login_admin(payload)


class TestCustomerRegistration:
    def test_register_customer_success(self, db_session: Session):
        svc = AuthService(db_session)
        payload = CustomerCreate(
            customer_name="New Customer",
            customer_email="newcust@test.com",
            customer_password="Cust12345",
        )
        cust = svc.register_customer(payload)
        assert cust.customer_id is not None
        assert cust.customer_password != "Cust12345"

    def test_register_duplicate_customer_email(self, db_session: Session, sample_customer):
        svc = AuthService(db_session)
        payload = CustomerCreate(
            customer_name="Dup",
            customer_email=sample_customer.customer_email,
            customer_password="Cust12345",
        )
        with pytest.raises(ConflictError):
            svc.register_customer(payload)


class TestCustomerLogin:
    def test_login_customer_success(self, db_session: Session, sample_customer):
        svc = AuthService(db_session)
        payload = CustomerLogin(
            customer_email=sample_customer.customer_email,
            customer_password="Cust12345",
        )
        tokens = svc.login_customer(payload)
        assert tokens.access_token
        assert tokens.role == "customer"
        assert tokens.user_id == sample_customer.customer_id

    def test_login_wrong_password(self, db_session: Session, sample_customer):
        svc = AuthService(db_session)
        payload = CustomerLogin(
            customer_email=sample_customer.customer_email,
            customer_password="Wrong12345",
        )
        with pytest.raises(AuthenticationError):
            svc.login_customer(payload)


class TestTokenRefresh:
    def test_refresh_valid_token(self, db_session: Session, sample_admin):
        svc = AuthService(db_session)
        login_payload = AdminLogin(
            admin_email=sample_admin.admin_email,
            admin_password="Admin1234",
        )
        tokens = svc.login_admin(login_payload)
        refreshed = svc.refresh_tokens(tokens.refresh_token)
        assert refreshed.access_token
        assert refreshed.refresh_token

    def test_refresh_with_access_token_fails(self, db_session: Session, sample_admin):
        svc = AuthService(db_session)
        login_payload = AdminLogin(
            admin_email=sample_admin.admin_email,
            admin_password="Admin1234",
        )
        tokens = svc.login_admin(login_payload)
        with pytest.raises(AuthenticationError):
            svc.refresh_tokens(tokens.access_token)

    def test_refresh_with_invalid_token(self, db_session: Session):
        svc = AuthService(db_session)
        with pytest.raises(AuthenticationError):
            svc.refresh_tokens("invalid.token.here")


class TestIssueTokens:
    def test_issue_tokens(self):
        tokens = AuthService._issue_tokens(user_id=99, role="customer")
        payload = decode_token(tokens.access_token)
        assert payload is not None
        assert payload["sub"] == "99"
        assert payload["role"] == "customer"
        assert tokens.user_id == 99
        assert tokens.role == "customer"
