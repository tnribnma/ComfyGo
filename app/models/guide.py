from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .booking import Booking


class Guide(TimestampMixin, Base):
    __tablename__ = "guides"

    guide_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guide_name: Mapped[str] = mapped_column(String(120), nullable=False)
    guide_email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    guide_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    guide_language: Mapped[str] = mapped_column(String(100), nullable=True)
    guide_experience: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="guide"
    )

    def __repr__(self) -> str:
        return f"<Guide id={self.guide_id} name={self.guide_name}>"