from datetime import date
from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep, CurrentCustomerDep
from ...schemas.package import TourPackageOut, TourPackageCreate, TourPackageUpdate
from ...schemas.package_booking import PackageBookingCreate, PackageBookingOut, PackageBookingUpdate
from ...schemas.common import PaginatedResponse
from ...services import TourPackageService
from ...services.package_booking_service import PackageBookingService

router = APIRouter(prefix="/packages", tags=["Tour Packages"])


@router.get("/", response_model=PaginatedResponse[TourPackageOut])
def list_packages(
    db: DBDep,
    destination: str = Query(None),
    country: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    difficulty: str = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    items = TourPackageService(db).search(
        destination=destination, country=country, min_price=min_price,
        max_price=max_price, difficulty=difficulty, skip=skip, limit=limit
    )
    return PaginatedResponse[TourPackageOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/{package_id}", response_model=TourPackageOut)
def get_package(package_id: int, db: DBDep):
    return TourPackageService(db).get(package_id)


@router.post("/", response_model=TourPackageOut, status_code=201)
def create_package(payload: TourPackageCreate, db: DBDep, _: CurrentAdminDep):
    return TourPackageService(db).create(payload)


@router.put("/{package_id}", response_model=TourPackageOut)
def update_package(package_id: int, payload: TourPackageUpdate, db: DBDep, _: CurrentAdminDep):
    return TourPackageService(db).update(package_id, payload)


@router.delete("/{package_id}", status_code=204)
def delete_package(package_id: int, db: DBDep, _: CurrentAdminDep):
    TourPackageService(db).delete(package_id)


@router.get("/{package_id}/availability")
def check_availability(package_id: int, travel_date: date, db: DBDep):
    """Check how many seats are left for a package on a specific date."""
    return PackageBookingService(db).get_available_seats(package_id, travel_date)


@router.post("/{package_id}/book", response_model=PackageBookingOut, status_code=201)
def book_package(
    package_id: int,
    payload: PackageBookingCreate,
    db: DBDep,
    user: CurrentCustomerDep,
):
    payload.package_id = package_id
    return PackageBookingService(db).create(customer_id=user.customer_id, payload=payload)


@router.get("/my-bookings", response_model=list[PackageBookingOut])
def my_package_bookings(db: DBDep, user: CurrentCustomerDep, skip: int = 0, limit: int = 50):
    """List the current customer's package bookings."""
    return PackageBookingService(db).get_customer_bookings(user.customer_id, skip=skip, limit=limit)


@router.post("/{booking_id}/cancel", response_model=PackageBookingOut)
def cancel_package_booking(booking_id: int, db: DBDep, user: CurrentCustomerDep):
    """Cancel a package booking."""
    return PackageBookingService(db).cancel(booking_id, user.customer_id)


@router.patch("/{booking_id}/status", response_model=PackageBookingOut)
def update_booking_status(
    booking_id: int, payload: PackageBookingUpdate, db: DBDep, _: CurrentAdminDep
):
    """Admin: update a booking's status or details."""
    return PackageBookingService(db).update_status(booking_id, payload)
