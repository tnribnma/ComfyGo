from typing import Sequence
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Employee
from .base import GenericRepository


class EmployeeRepository(GenericRepository[Employee]):
    model = Employee

    def get_by_email(self, email: str):
        stmt = select(Employee).where(Employee.employee_email == email)
        return self.db.scalars(stmt).first()

    def list_by_hotel(
        self, hotel_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Employee]:
        stmt = (
            select(Employee)
            .where(Employee.hotel_id == hotel_id)
            .order_by(Employee.employee_name)
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_admin(
        self, admin_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Employee]:
        stmt = (
            select(Employee)
            .where(Employee.admin_id == admin_id)
            .order_by(Employee.employee_name)
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def count_by_hotel(self, hotel_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Employee)
            .where(Employee.hotel_id == hotel_id)
        )
        return int(self.db.scalar(stmt) or 0)

    def count_by_admin(self, admin_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Employee)
            .where(Employee.admin_id == admin_id)
        )
        return int(self.db.scalar(stmt) or 0)