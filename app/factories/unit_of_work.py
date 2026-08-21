from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from ..repositories import (
    AdminRepository, EmployeeRepository, HotelRepository,
    CustomerRepository, GuideRepository, BookingRepository,
    PaymentRepository, AuditLogRepository
)


class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db
        self.admins = AdminRepository(db)
        self.admins.auto_commit = False

        self.employees = EmployeeRepository(db)
        self.employees.auto_commit = False

        self.hotels = HotelRepository(db)
        self.hotels.auto_commit = False

        self.customers = CustomerRepository(db)
        self.customers.auto_commit = False

        self.guides = GuideRepository(db)
        self.guides.auto_commit = False

        self.bookings = BookingRepository(db)
        self.bookings.auto_commit = False

        self.payments = PaymentRepository(db)
        self.payments.auto_commit = False

        self.audit_logs = AuditLogRepository(db)
        self.audit_logs.auto_commit = False

    def __enter__(self) -> "UnitOfWork":
        self.db.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.db.rollback()
        else:
            self.db.commit()

    @property
    @contextmanager
    def transaction(self) -> Generator["UnitOfWork", None, None]:
        try:
            yield self
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise