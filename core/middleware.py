import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from ..config import settings
from .exceptions import AppException
from .logger import get_logger

log = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Reads `X-Request-ID` from the request, or generates a UUID4.
    Stores it on `request.state.request_id` and echoes it back as a response header.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs `request_id | METHOD /path | status | duration_ms` for every request,
    including unhandled exceptions.
    """
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


def register_middleware(app: FastAPI) -> None:
    """
    Wire all middleware. Order of add_middleware calls matters:
      - added LAST = outermost = runs FIRST on request
    We want RequestID outermost (so Logging has request_id available).
    """
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)  


def register_exception_handlers(app: FastAPI) -> None:
    """Map domain & framework exceptions to consistent JSON envelopes."""

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
        log.info("%s | Validation error: %s", request_id, exc.errors())
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "message": "Request validation failed",
                "detail": exc.errors(),
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