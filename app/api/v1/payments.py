from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentCustomerDep, CurrentAdminDep
from ...schemas.payment import PaymentOut, PaymentCreate, PaymentStatusUpdate
from ...schemas.common import PaginatedResponse
from ...services import PaymentService, BookingService

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/", response_model=PaginatedResponse[PaymentOut])
def list_payments(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    from ...repositories import PaymentRepository
    repo = PaymentRepository(db)
    items = repo.get_multi(skip=skip, limit=limit)
    return PaginatedResponse[PaymentOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.post("/", response_model=PaymentOut, status_code=201)
def process_payment(payload: PaymentCreate, db: DBDep, user: CurrentCustomerDep):
    booking = BookingService(db).get(payload.booking_id)
    if booking.customer_id != user.customer_id:
        from ...core.exceptions import AuthorizationError
        raise AuthorizationError("Cannot pay for a booking you do not own.")
    return PaymentService(db).process_payment(payload)

@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: DBDep, _: CurrentAdminDep):
    return PaymentService(db).get(payment_id)

@router.get("/booking/{booking_id}", response_model=PaymentOut)
def get_booking_payment(booking_id: int, db: DBDep, _: CurrentAdminDep):
    return PaymentService(db).get_by_booking(booking_id)

@router.post("/{payment_id}/refund", response_model=PaymentOut)
def refund_payment(payment_id: int, db: DBDep, _: CurrentAdminDep):
    return PaymentService(db).refund(payment_id)