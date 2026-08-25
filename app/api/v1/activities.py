from datetime import date
from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep, CurrentCustomerDep
from ...schemas.activity import ActivityOut, ActivityCreate, ActivityUpdate
from ...schemas.activity_booking import ActivityBookingCreate, ActivityBookingOut, ActivityBookingUpdate
from ...schemas.common import PaginatedResponse
from ...services import ActivityService
from ...services.activity_booking_service import ActivityBookingService

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("/", response_model=PaginatedResponse[ActivityOut])
def list_activities(
    db: DBDep,
    destination: str = Query(None),
    category: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    difficulty: str = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    items = ActivityService(db).search(
        destination=destination, category=category, min_price=min_price,
        max_price=max_price, difficulty=difficulty, skip=skip, limit=limit
    )
    return PaginatedResponse[ActivityOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity(activity_id: int, db: DBDep):
    return ActivityService(db).get(activity_id)


@router.post("/", response_model=ActivityOut, status_code=201)
def create_activity(payload: ActivityCreate, db: DBDep, _: CurrentAdminDep):
    return ActivityService(db).create(payload)


@router.put("/{activity_id}", response_model=ActivityOut)
def update_activity(activity_id: int, payload: ActivityUpdate, db: DBDep, _: CurrentAdminDep):
    return ActivityService(db).update(activity_id, payload)


@router.delete("/{activity_id}", status_code=204)
def delete_activity(activity_id: int, db: DBDep, _: CurrentAdminDep):
    ActivityService(db).delete(activity_id)


@router.get("/{activity_id}/availability")
def check_availability(activity_id: int, booking_date: date, db: DBDep):
    """Check available spots for an activity on a specific date."""
    return ActivityBookingService(db).get_available_spots(activity_id, booking_date)


@router.post("/{activity_id}/book", response_model=ActivityBookingOut, status_code=201)
def book_activity(
    activity_id: int,
    payload: ActivityBookingCreate,
    db: DBDep,
    user: CurrentCustomerDep,
):
   
    payload.activity_id = activity_id
    return ActivityBookingService(db).create(customer_id=user.customer_id, payload=payload)


@router.get("/my-bookings", response_model=list[ActivityBookingOut])
def my_activity_bookings(db: DBDep, user: CurrentCustomerDep, skip: int = 0, limit: int = 50):
    """List the current customer's activity bookings."""
    return ActivityBookingService(db).get_customer_bookings(user.customer_id, skip=skip, limit=limit)


@router.post("/{booking_id}/cancel", response_model=ActivityBookingOut)
def cancel_activity_booking(booking_id: int, db: DBDep, user: CurrentCustomerDep):
    """Cancel an activity booking."""
    return ActivityBookingService(db).cancel(booking_id, user.customer_id)


@router.patch("/{booking_id}/status", response_model=ActivityBookingOut)
def update_booking_status(
    booking_id: int, payload: ActivityBookingUpdate, db: DBDep, _: CurrentAdminDep
):
    """Admin: update a booking's status or details."""
    return ActivityBookingService(db).update_status(booking_id, payload)
