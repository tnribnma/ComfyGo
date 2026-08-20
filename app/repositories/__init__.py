from .base import GenericRepository
from .admin_repository import AdminRepository
from .employee_repository import EmployeeRepository
from .hotel_repository import HotelRepository
from .customer_repository import CustomerRepository
from .guide_repository import GuideRepository
from .booking_repository import BookingRepository
from .payment_repository import PaymentRepository

__all__ = [
    "GenericRepository",
    "AdminRepository",
    "EmployeeRepository",
    "HotelRepository",
    "CustomerRepository",
    "GuideRepository",
    "BookingRepository",
    "PaymentRepository",
]