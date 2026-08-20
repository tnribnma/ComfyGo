from typing import Optional


class AppException(Exception):
    http_status: int = 400
    code: str = "app_error"

    def __init__(self, message: str, detail: Optional[str] = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)


class NotFoundError(AppException):
    http_status = 404
    code = "not_found"


class ConflictError(AppException):
    """E.g. duplicate email."""
    http_status = 409
    code = "conflict"


class ValidationError(AppException):
    http_status = 422
    code = "validation_error"


class AuthenticationError(AppException):
    http_status = 401
    code = "authentication_failed"


class AuthorizationError(AppException):
    http_status = 403
    code = "forbidden"


class BusinessRuleError(AppException):
    http_status = 409
    code = "business_rule_violation"