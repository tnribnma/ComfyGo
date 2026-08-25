from sqlalchemy import String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base, TimestampMixin


class Review(TimestampMixin, Base):
    __tablename__ = "reviews"

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.customer_id"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) 
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False) 
    title: Mapped[str] = mapped_column(String(200), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    verified_visit: Mapped[bool] = mapped_column(default=False)
    photos: Mapped[str] = mapped_column(Text, nullable=True)  
    owner_response: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Review id={self.review_id} rating={self.rating}>"
