from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentCustomerDep, CurrentAdminDep
from ...schemas.booking import BookingOut, BookingCreate, BookingUpdate
from ...schemas.common import PaginatedResponse
from ...services import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", response_model=PaginatedResponse[BookingOut])
def list_bookings(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    items = BookingService(db).list(skip=skip, limit=limit)
    return PaginatedResponse[BookingOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.post("/", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: DBDep, user: CurrentCustomerDep):
    payload.customer_id = user.customer_id
    return BookingService(db).create(payload)

@router.get("/my-bookings", response_model=PaginatedResponse[BookingOut])
def my_bookings(db: DBDep, user: CurrentCustomerDep, skip: int = 0, limit: int = 100):
    items = BookingService(db).list_by_customer(user.customer_id, skip=skip, limit=limit)
    return PaginatedResponse[BookingOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: DBDep, user: CurrentCustomerDep):
    booking = BookingService(db).get(booking_id)
    if user.customer_id != booking.customer_id:
        from ...core.exceptions import AuthorizationError
        raise AuthorizationError("You can only view your own bookings")
    return booking

@router.put("/{booking_id}", response_model=BookingOut)
def update_booking(booking_id: int, payload: BookingUpdate, db: DBDep, _: CurrentAdminDep):
    return BookingService(db).update(booking_id, payload)

@router.post("/{booking_id}/confirm", response_model=BookingOut)
def confirm_booking(booking_id: int, db: DBDep, _: CurrentAdminDep):
    return BookingService(db).confirm(booking_id)

@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: int, db: DBDep, _: CurrentAdminDep):
    return BookingService(db).cancel(booking_id)

@router.post("/{booking_id}/complete", response_model=BookingOut)
def complete_booking(booking_id: int, db: DBDep, _: CurrentAdminDep):
    return BookingService(db).complete(booking_id)

@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: DBDep, _: CurrentAdminDep):
    BookingService(db).delete(booking_id)