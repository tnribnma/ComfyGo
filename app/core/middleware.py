import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from ..config import settings
from .exceptions import AppException
from .logger import get_logger
from ..database import Database
from ..repositories.audit_log_repository import AuditLogRepository

log = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    SKIP_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json"}

    async def dispatch(self, request: Request, call_next: Callable):
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        request_id = getattr(request.state, "request_id", "-")
        method = request.method
        path = request.url.path
        client = request.client.host if request.client else "-"

        start = time.perf_counter()
        try:
            response: Response = await call_next(request)
            duration_ms = (time.perf_counter() - start) * 1000
            if response.status_code >= 400 or method != "GET":
                log.info(
                    "%s | %s %s | %s | %.2fms | client=%s",
                    request_id, method, path,
                    response.status_code, duration_ms, client,
                )
            return response
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            log.exception(
                "%s | %s %s | ERROR | %.2fms | client=%s | %s",
                request_id, method, path, duration_ms, client, exc,
            )
            raise


class AuditMiddleware(BaseHTTPMiddleware):
    SKIP_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json"}

    async def dispatch(self, request: Request, call_next: Callable):
        if request.url.path in self.SKIP_PATHS or request.method in ("GET", "OPTIONS"):
            return await call_next(request)

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        user_id = None
        user_role = None
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            from .security import decode_token
            token = auth_header[7:]
            payload = decode_token(token)
            if payload:
                try:
                    user_id = int(payload["sub"]) if payload.get("sub") else None
                except (TypeError, ValueError):
                    user_id = None
                user_role = payload.get("role")

        method = request.method
        action_map = {
            "POST": "CREATE",
            "PUT": "UPDATE",
            "PATCH": "UPDATE",
            "DELETE": "DELETE",
        }
        action = action_map.get(method, method.upper())

        db = None
        try:
            db = Database.session_factory()()
            repo = AuditLogRepository(db)
            repo.create({
                "user_id": user_id,
                "user_role": user_role,
                "action": action,
                "entity_type": self._guess_entity(request.url.path),
                "request_method": method,
                "request_path": request.url.path,
                "status_code": response.status_code,
                "ip_address": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent", "")[:500],
                "duration_ms": round(duration_ms, 2),
            })
        except Exception as e:
            log.error("Failed to write audit log: %s", e)
        finally:
            if db is not None:
                db.close()

        return response

    @staticmethod
    def _guess_entity(path: str) -> str:
        parts = path.strip("/").split("/")
        if len(parts) >= 3 and parts[0] == "api":
            entity = parts[2]
            return entity.rstrip("s").capitalize()
        return None


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(AuditMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def _app_exception(request: Request, exc: AppException):
        request_id = getattr(request.state, "request_id", "-")
        log.warning(
            "%s | AppException %s: %s (%s)",
            request_id, exc.code, exc.message, exc.detail,
        )
        return JSONResponse(
            status_code=exc.http_status,
            content={
                "error": exc.code,
                "message": exc.message,
                "detail": exc.detail,
                "request_id": request_id,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_exception(request: Request, exc: RequestValidationError):
        request_id = getattr(request.state, "request_id", "-")

        safe_errors = []
        for err in exc.errors():
            e = err.copy()
            if "ctx" in e and "error" in e["ctx"]:
                e["ctx"]["error"] = str(e["ctx"]["error"])
            safe_errors.append(e)

        log.info("%s | Validation error: %s", request_id, safe_errors)
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "message": "Request validation failed",
                "detail": safe_errors,
                "request_id": request_id,
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def _db_exception(request: Request, exc: SQLAlchemyError):
        request_id = getattr(request.state, "request_id", "-")
        log.exception("%s | Database error: %s", request_id, exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "database_error",
                "message": (
                    "Internal database error"
                    if settings.is_production else str(exc)
                ),
                "request_id": request_id,
            },
        )

    @app.exception_handler(Exception)
    async def _unhandled_exception(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "-")
        log.exception("%s | Unhandled exception: %s", request_id, exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": (
                    "Internal server error"
                    if settings.is_production else str(exc)
                ),
                "request_id": request_id,
            },
        )
