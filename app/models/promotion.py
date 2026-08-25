from sqlalchemy import String, Integer, Numeric, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base, TimestampMixin


class Promotion(TimestampMixin, Base):
    __tablename__ = "promotions"

    promotion_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    destination: Mapped[str] = mapped_column(String(100), nullable=True)
    original_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    discount_percent: Mapped[int] = mapped_column(Integer, nullable=True)
    final_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    promo_code: Mapped[str] = mapped_column(String(50), nullable=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    badge: Mapped[str] = mapped_column(String(50), nullable=True)  
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"<Promotion id={self.promotion_id} title={self.title}>"
