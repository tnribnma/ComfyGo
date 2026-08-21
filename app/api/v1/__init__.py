from fastapi import APIRouter

from .auth import router as auth_router
from .admins import router as admins_router
from .employees import router as employees_router
from .hotels import router as hotels_router
from .customers import router as customers_router
from .guides import router as guides_router
from .bookings import router as bookings_router
from .payments import router as payments_router
from .admin import router as admin_panel_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(admin_panel_router)

router.include_router(admins_router)
router.include_router(employees_router)
router.include_router(hotels_router)
router.include_router(customers_router)
router.include_router(guides_router)
router.include_router(bookings_router)
router.include_router(payments_router)

__all__ = ["router"]