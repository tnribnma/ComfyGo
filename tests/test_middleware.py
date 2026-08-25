import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import date, timedelta

from app.main import app
from app.database import Database, get_db
from app.core.middleware import AuditMiddleware, RequestIDMiddleware, RequestLoggingMiddleware
from app.core.exceptions import (
    AppException, NotFoundError, ConflictError,
    ValidationError, BusinessRuleError,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class TestRequestIDMiddleware:
    def test_generates_request_id_when_missing(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            resp = client.get("/")
            assert "X-Request-ID" in resp.headers
            assert len(resp.headers["X-Request-ID"]) > 0

    def test_preserves_existing_request_id(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            custom_id = "my-custom-request-id-123"
            resp = client.get("/", headers={"X-Request-ID": custom_id})
            assert resp.headers["X-Request-ID"] == custom_id

    def test_request_id_on_health(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            resp = client.get("/health")
            assert "X-Request-ID" in resp.headers

class TestAppExceptionHandler:
    def test_not_found_error(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            resp = client.get(
                "/api/v1/hotels/999999",
                headers={"Authorization": "Bearer invalid"},
            )
            assert resp.status_code in (401, 404)

    def test_validation_error_format(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            resp = client.post(
                "/api/v1/auth/register/customer",
                json={"bad": "data"},
            )
            assert resp.status_code == 422
            body = resp.json()
            assert body["error"] == "validation_error"


class TestExceptionClasses:
    def test_app_exception_handler_returns_json(self):
        exc = AppException("test", detail="extra")
        assert exc.http_status == 400
        assert exc.code == "app_error"

    def test_not_found_exception(self):
        exc = NotFoundError("missing")
        assert exc.http_status == 404
        assert exc.code == "not_found"

    def test_conflict_exception(self):
        exc = ConflictError("dup")
        assert exc.http_status == 409

    def test_business_rule_exception(self):
        exc = BusinessRuleError("rule broken")
        assert exc.http_status == 409
        assert exc.code == "business_rule_violation"


class TestAuditGuessEntity:
    def test_guess_entity_from_path(self):
        assert AuditMiddleware._guess_entity("/api/v1/hotels") == "Hotel"
        assert AuditMiddleware._guess_entity("/api/v1/bookings") == "Booking"
        assert AuditMiddleware._guess_entity("/api/v1/customers") == "Customer"

    def test_guess_entity_short_path(self):
        assert AuditMiddleware._guess_entity("/health") is None

    def test_guess_entity_root(self):
        assert AuditMiddleware._guess_entity("/") is None


class TestRequestLoggingSkips:
    def test_health_not_skipped_in_response(self):
        """Health should return 200 — it's in SKIP_PATHS but still works."""
        with TestClient(app, raise_server_exceptions=False) as client:
            resp = client.get("/health")
            assert resp.status_code == 200
            body = resp.json()
            assert body["status"] in ("ok", "degraded")


class TestHealthEndpoint:
    def test_health_returns_ok(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            resp = client.get("/health")
            assert resp.status_code == 200
            body = resp.json()
            assert "status" in body
            assert "version" in body
            assert "env" in body
