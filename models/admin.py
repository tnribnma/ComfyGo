"""
Admin model — top-level user who manages hotels & employees.
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .employee import Employee


class Admin(TimestampMixin, Base):
    __tablename__ = "admins"

    admin_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_name: Mapped[str] = mapped_column(String(120), nullable=False)
    admin_email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    admin_password: Mapped[str] = mapped_column(String(255), nullable=False)
    admin_phone: Mapped[str] = mapped_column(String(20), nullable=True)

    # One-to-many: Admin -> Employees
    employees: Mapped[List["Employee"]] = relationship(
        "Employee",
        back_populates="admin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Admin id={self.admin_id} email={self.admin_email}>"