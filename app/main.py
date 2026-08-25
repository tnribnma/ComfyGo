from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from . import __version__
from .config import settings
from .database import Database
from .core.logger import get_logger
from .core.middleware import register_middleware, register_exception_handlers
from .api.router import api_router

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting %s v%s (env=%s)", settings.APP_NAME, __version__, settings.APP_ENV)
    log.info("Database URL: %s", settings.database_url)
    Database.engine()               
    if settings.APP_DEBUG:
        Database.create_all()         
    yield
    log.info("Shutting down — disposing DB pool")
    Database.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=__version__,
        description="ComfyGo — Hotel & Travel Booking API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )
    register_middleware(app)             
    register_exception_handlers(app)    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/", include_in_schema=False)
    def root():
        return {"app": settings.APP_NAME, "version": __version__, "docs": "/docs"}

    @app.get("/health", tags=["health"])
    def health():
        try:
            Database.engine().connect().close()
            db_ok = True
        except Exception as e:
            log.error("Health DB ping failed: %s", e)
            db_ok = False
        return {
            "status": "ok" if db_ok else "degraded",
            "database": db_ok,
            "version": __version__,
            "env": settings.APP_ENV,
        }

    return app


app = create_app()