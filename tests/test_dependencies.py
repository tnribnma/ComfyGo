import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.dependencies import (
    get_current_user,
    require_admin,
    require_employee,
    require_customer,
    get_optional_user,
    _require_role,
)
from app.models import Admin, Employee, Customer
from app.core.security import create_access_token


class TestGetCurrentUser:
    def test_valid_admin_token(self, db_session, sample_admin):
        token = create_access_token(
            subject=str(sample_admin.admin_id), role="admin"
        )
        user = get_current_user(token=token, db=db_session)
        assert isinstance(user, Admin)
        assert user.admin_id == sample_admin.admin_id

    def test_valid_customer_token(self, db_session, sample_customer):
        token = create_access_token(
            subject=str(sample_customer.customer_id), role="customer"
        )
        user = get_current_user(token=token, db=db_session)
        assert isinstance(user, Customer)
        assert user.customer_id == sample_customer.customer_id

    def test_invalid_token(self, db_session):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="bad.token.value", db=db_session)
        assert exc_info.value.status_code == 401

    def test_token_with_wrong_role(self, db_session, sample_admin):
        token = create_access_token(
            subject=str(sample_admin.admin_id), role="customer"
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=db_session)
        assert exc_info.value.status_code == 401

    def test_nonexistent_user(self, db_session):
        token = create_access_token(subject="999999", role="admin")
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=db_session)
        assert exc_info.value.status_code == 401

    def test_malformed_sub(self, db_session):
        from jose import jwt
        from app.config import settings
        token = jwt.encode(
            {"sub": "not-a-number", "role": "admin", "type": "access"},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALG,
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=db_session)
        assert exc_info.value.status_code == 401

    def test_refresh_token_rejected(self, db_session, sample_admin):
        from app.core.security import create_refresh_token
        token = create_refresh_token(
            subject=str(sample_admin.admin_id), role="admin"
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=db_session)
        assert exc_info.value.status_code == 401


class TestRequireRole:
    def test_require_admin_passes(self, db_session, sample_admin):
        user = require_admin(user=sample_admin)
        assert user.admin_id == sample_admin.admin_id

    def test_require_admin_fails_for_customer(self, db_session, sample_customer):
        with pytest.raises(HTTPException) as exc_info:
            require_admin(user=sample_customer)
        assert exc_info.value.status_code == 403

    def test_require_employee_fails_for_admin(self, db_session, sample_admin):
        with pytest.raises(HTTPException) as exc_info:
            require_employee(user=sample_admin)
        assert exc_info.value.status_code == 403

    def test_require_customer_fails_for_admin(self, db_session, sample_admin):
        with pytest.raises(HTTPException) as exc_info:
            require_customer(user=sample_admin)
        assert exc_info.value.status_code == 403


class TestRequireAdmin:
    def test_passes_for_admin(self, db_session, sample_admin):
        result = require_admin(user=sample_admin)
        assert result.admin_id == sample_admin.admin_id

    def test_rejects_customer(self, db_session, sample_customer):
        with pytest.raises(HTTPException) as exc_info:
            require_admin(user=sample_customer)
        assert exc_info.value.status_code == 403
        assert "Admin" in exc_info.value.detail


class TestRequireEmployee:
    def test_rejects_admin(self, db_session, sample_admin):
        with pytest.raises(HTTPException) as exc_info:
            require_employee(user=sample_admin)
        assert exc_info.value.status_code == 403
        assert "Employee" in exc_info.value.detail


class TestRequireCustomer:
    def test_rejects_admin(self, db_session, sample_admin):
        with pytest.raises(HTTPException) as exc_info:
            require_customer(user=sample_admin)
        assert exc_info.value.status_code == 403
        assert "Customer" in exc_info.value.detail


class TestGetOptionalUser:
    def test_returns_none_when_no_token(self):
        result = get_optional_user(token=None, db=None)
        assert result is None

    def test_returns_user_when_valid(self, db_session, sample_admin):
        token = create_access_token(
            subject=str(sample_admin.admin_id), role="admin"
        )
        result = get_optional_user(token=token, db=db_session)
        assert result is not None
        assert isinstance(result, Admin)

    def test_returns_none_when_invalid(self, db_session):
        result = get_optional_user(token="bad.token", db=db_session)
        assert result is None
