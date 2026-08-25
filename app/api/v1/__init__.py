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
from .tourist_spots import router as tourist_spots_router
from .rooms import router as rooms_router
from .reviews import router as reviews_router
from .packages import router as packages_router
from .activities import router as activities_router
from .restaurants import router as restaurants_router
from .flights import router as flights_router
from .local_transport import router as local_transport_router
from .promotions import router as promotions_router

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
router.include_router(tourist_spots_router)
router.include_router(rooms_router)
router.include_router(reviews_router)
router.include_router(packages_router)
router.include_router(activities_router)
router.include_router(restaurants_router)
router.include_router(flights_router)
router.include_router(local_transport_router)
router.include_router(promotions_router)

__all__ = ["router"]
