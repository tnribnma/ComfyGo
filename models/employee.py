from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .admin import Admin
    from .hotel import Hotel


class Employee(TimestampMixin, Base):
    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    employee_name: Mapped[str] = mapped_column(String(120), nullable=False)
    employee_email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    employee_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    employee_position: Mapped[str] = mapped_column(String(100), nullable=True)
    employee_password: Mapped[str] = mapped_column(String(255), nullable=False)

    hotel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("hotels.hotel_id", ondelete="CASCADE"), nullable=False,
        index=True,
    )
    admin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("admins.admin_id", ondelete="CASCADE"), nullable=False,
        index=True,
    )

    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="employees")
    admin: Mapped["Admin"] = relationship("Admin", back_populates="employees")

    def __repr__(self) -> str:
        return f"<Employee id={self.employee_id} email={self.employee_email}>"