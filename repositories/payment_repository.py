from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Payment, PaymentMethod, PaymentStatus
from .base import GenericRepository


class PaymentRepository(GenericRepository[Payment]):
    model = Payment

    def get_by_booking(self, booking_id: int) -> Optional[Payment]:
        stmt = select(Payment).where(Payment.booking_id == booking_id)
        return self.db.scalars(stmt).first()

    def get_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        stmt = select(Payment).where(Payment.transaction_id == transaction_id)
        return self.db.scalars(stmt).first()

    def list_by_status(
        self, status: PaymentStatus, skip: int = 0, limit: int = 100
    ) -> Sequence[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.payment_status == status)
            .order_by(Payment.payment_date.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_method(
        self, method: PaymentMethod, skip: int = 0, limit: int = 100
    ) -> Sequence[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.payment_method == method)
            .order_by(Payment.payment_date.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()