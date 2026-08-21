from sqlalchemy.orm import Session

from ..repositories import (
    AdminRepository,
    EmployeeRepository,
    HotelRepository,
    CustomerRepository,
    GuideRepository,
    BookingRepository,
    PaymentRepository,
    AuditLogRepository,
)

class RepositoryFactory:

    def __init__(self, db: Session):
        self.db = db

    def admin(self) -> AdminRepository:
        return AdminRepository(self.db)

    def employee(self) -> EmployeeRepository:
        return EmployeeRepository(self.db)

    def hotel(self) -> HotelRepository:
        return HotelRepository(self.db)

    def customer(self) -> CustomerRepository:
        return CustomerRepository(self.db)

    def guide(self) -> GuideRepository:
        return GuideRepository(self.db)

    def booking(self) -> BookingRepository:
        return BookingRepository(self.db)

    def payment(self) -> PaymentRepository:
        return PaymentRepository(self.db)

    def audit_log(self) -> AuditLogRepository:
        return AuditLogRepository(self.db)