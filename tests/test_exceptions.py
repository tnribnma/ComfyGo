import pytest
from app.core.exceptions import (
    AppException,
    NotFoundError,
    ConflictError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    BusinessRuleError,
)


class TestAppException:
    def test_base_exception(self):
        exc = AppException("Something went wrong", detail="extra info")
        assert str(exc) == "Something went wrong"
        assert exc.message == "Something went wrong"
        assert exc.detail == "extra info"
        assert exc.http_status == 400
        assert exc.code == "app_error"

    def test_base_exception_no_detail(self):
        exc = AppException("Oops")
        assert exc.detail is None

    def test_inherits_from_exception(self):
        assert issubclass(AppException, Exception)
        with pytest.raises(AppException):
            raise AppException("test")


class TestNotFoundError:
    def test_attributes(self):
        exc = NotFoundError("Not here", detail="id=5")
        assert exc.http_status == 404
        assert exc.code == "not_found"
        assert exc.message == "Not here"
        assert exc.detail == "id=5"

    def test_is_app_exception(self):
        assert issubclass(NotFoundError, AppException)


class TestConflictError:
    def test_attributes(self):
        exc = ConflictError("Duplicate email", detail="a@b.com")
        assert exc.http_status == 409
        assert exc.code == "conflict"
        assert issubclass(ConflictError, AppException)


class TestValidationError:
    def test_attributes(self):
        exc = ValidationError("Bad input", detail="field X invalid")
        assert exc.http_status == 422
        assert exc.code == "validation_error"
        assert issubclass(ValidationError, AppException)


class TestAuthenticationError:
    def test_attributes(self):
        exc = AuthenticationError("Wrong password")
        assert exc.http_status == 401
        assert exc.code == "authentication_failed"
        assert issubclass(AuthenticationError, AppException)


class TestAuthorizationError:
    def test_attributes(self):
        exc = AuthorizationError("No access")
        assert exc.http_status == 403
        assert exc.code == "forbidden"
        assert issubclass(AuthorizationError, AppException)


class TestBusinessRuleError:
    def test_attributes(self):
        exc = BusinessRuleError("Cannot cancel", detail="already confirmed")
        assert exc.http_status == 409
        assert exc.code == "business_rule_violation"
        assert issubclass(BusinessRuleError, AppException)
