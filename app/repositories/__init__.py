from .base import GenericRepository
from .admin_repository import AdminRepository
from .employee_repository import EmployeeRepository
from .hotel_repository import HotelRepository
from .customer_repository import CustomerRepository
from .guide_repository import GuideRepository
from .booking_repository import BookingRepository
from .payment_repository import PaymentRepository
from .tourist_spot_repository import TouristSpotRepository
from .room_repository import RoomRepository
from .review_repository import ReviewRepository
from .package_repository import TourPackageRepository
from .activity_repository import ActivityRepository
from .restaurant_repository import RestaurantRepository
from .flight_repository import FlightRepository
from .local_transport_repository import LocalTransportRepository
from .promotion_repository import PromotionRepository

__all__ = [
    "GenericRepository",
    "AdminRepository",
    "EmployeeRepository",
    "HotelRepository",
    "CustomerRepository",
    "GuideRepository",
    "BookingRepository",
    "PaymentRepository",
    "TouristSpotRepository",
    "RoomRepository",
    "ReviewRepository",
    "TourPackageRepository",
    "ActivityRepository",
    "RestaurantRepository",
    "FlightRepository",
    "LocalTransportRepository",
    "PromotionRepository",
]
