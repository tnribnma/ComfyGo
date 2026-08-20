from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from ..models import PaymentStatus, BookingStatus
from ..repositories import PaymentRepository, BookingRepository
from ..schemas.payment import PaymentCreate, PaymentUpdate, PaymentStatusUpdate
from ..strategies.payment_factory import PaymentFactory


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PaymentRepository(db)
        self.booking_repo = BookingRepository(db)

    def get(self, payment_id: int):
        return self.repo.get_or_404(payment_id)

    def get_by_booking(self, booking_id: int):
        payment = self.repo.get_by_booking(booking_id)
        if payment is None:
            raise NotFoundError("Payment not found for this booking", detail=f"booking_id={booking_id}")
        return payment

    def list_by_status(self, status: PaymentStatus, skip: int = 0, limit: int = 100):
        return self.repo.list_by_status(status, skip=skip, limit=limit)

    def process_payment(self, payload: PaymentCreate):
        booking = self.booking_repo.get_or_404(payload.booking_id)

        if booking.booking_status == BookingStatus.CANCELLED:
            raise BusinessRuleError(
                "Cannot process payment for a cancelled booking",
                detail=f"booking_id={payload.booking_id}",
            )

        existing = self.repo.get_by_booking(payload.booking_id)
        if existing:
            raise ConflictError(
                "Payment already exists for this booking",
                detail=f"payment_id={existing.payment_id}",
            )

        strategy = PaymentFactory.create(payload.payment_method.value)
        result = strategy.pay(
            amount=payload.payment_amount,
            transaction_id=payload.transaction_id,
        )

        data = payload.model_dump()
        data["payment_status"] = PaymentStatus.SUCCESS if result["success"] else PaymentStatus.FAILED
        data["payment_date"] = datetime.now(timezone.utc)

        payment = self.repo.create(data)

        if result["success"] and booking.booking_status == BookingStatus.PENDING:
            self.booking_repo.update(payload.booking_id, {"booking_status": BookingStatus.CONFIRMED})

        return payment

    _VALID_PAYMENT_TRANSITIONS = {
        PaymentStatus.PENDING:  {PaymentStatus.SUCCESS, PaymentStatus.FAILED},
        PaymentStatus.SUCCESS:  {PaymentStatus.REFUNDED},
        PaymentStatus.FAILED:   set(),
        PaymentStatus.REFUNDED: set(),
    }

    def update_status(self, payment_id: int, payload: PaymentStatusUpdate):
        payment = self.repo.get_or_404(payment_id)
        current = payment.payment_status
        new_status = payload.payment_status

        if current == new_status:
            return payment

        allowed = self._VALID_PAYMENT_TRANSITIONS.get(current, set())
        if new_status not in allowed:
            raise BusinessRuleError(
                f"Cannot transition payment from {current.value} to {new_status.value}",
                detail=f"payment_id={payment_id}",
            )
        return self.repo.update(payment_id, {"payment_status": new_status})

    def refund(self, payment_id: int):
        """Convenience method — marks a successful payment as refunded."""
        return self.update_status(payment_id, PaymentStatusUpdate(payment_status=PaymentStatus.REFUNDED))

    def update(self, payment_id: int, payload: PaymentUpdate):
        return self.repo.update(payment_id, payload.model_dump(exclude_unset=True))