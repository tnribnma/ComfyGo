from fastapi import APIRouter, Query
from sqlalchemy import select
from ...dependencies import DBDep, CurrentAdminDep, CurrentCustomerDep
from ...schemas.customer import CustomerOut, CustomerCreate, CustomerUpdate
from ...schemas.common import PaginatedResponse
from ...services import CustomerService
from ...models import Booking, Hotel, Guide, PackageBooking, TourPackage, ActivityBooking, Activity, Review, Payment

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=PaginatedResponse[CustomerOut])
def list_customers(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    items = CustomerService(db).list(skip=skip, limit=limit)
    return PaginatedResponse[CustomerOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(payload: CustomerCreate, db: DBDep):
    return CustomerService(db).create(payload)

@router.get("/me", response_model=CustomerOut)
def get_my_profile(user: CurrentCustomerDep):
    return user

@router.put("/me", response_model=CustomerOut)
def update_my_profile(payload: CustomerUpdate, db: DBDep, user: CurrentCustomerDep):
    return CustomerService(db).update(user.customer_id, payload)

@router.get("/me/dashboard")
def my_dashboard(db: DBDep, user: CurrentCustomerDep):
    cid = user.customer_id

    profile = {
        "customer_id": cid,
        "name": user.customer_name,
        "email": user.customer_email,
        "phone": user.customer_phone,
        "address": user.customer_address,
        "member_since": user.created_at.isoformat() if user.created_at else None,
    }

    stmt = (
        select(
            Booking.booking_id, Booking.check_in_date, Booking.check_out_date,
            Booking.number_of_guests, Booking.total_amount, Booking.booking_status,
            Booking.created_at, Hotel.hotel_name, Hotel.hotel_city, Hotel.hotel_country,
            Guide.guide_name,
        )
        .outerjoin(Hotel, Booking.hotel_id == Hotel.hotel_id)
        .outerjoin(Guide, Booking.guide_id == Guide.guide_id)
        .where(Booking.customer_id == cid)
        .order_by(Booking.created_at.desc().nulls_last())
    )
    hotel_bookings = []
    for row in db.execute(stmt).all():
        hotel_bookings.append({
            "booking_id": row.booking_id,
            "hotel_name": row.hotel_name or "Hotel",
            "city": row.hotel_city or "",
            "country": row.hotel_country or "",
            "guide_name": row.guide_name,
            "check_in": str(row.check_in_date),
            "check_out": str(row.check_out_date),
            "guests": row.number_of_guests,
            "amount": float(row.total_amount),
            "status": row.booking_status.value if row.booking_status else "pending",
            "booked_at": row.created_at.isoformat() if row.created_at else None,
        })

    stmt = (
        select(
            PackageBooking.id, PackageBooking.booking_ref, PackageBooking.travel_date,
            PackageBooking.num_persons, PackageBooking.total_amount, PackageBooking.status,
            PackageBooking.created_at, TourPackage.package_name, TourPackage.destination,
        )
        .outerjoin(TourPackage, PackageBooking.package_id == TourPackage.package_id)
        .where(PackageBooking.customer_id == cid)
        .order_by(PackageBooking.created_at.desc().nulls_last())
    )
    pkg_bookings = []
    for row in db.execute(stmt).all():
        pkg_bookings.append({
            "id": row.id,
            "ref": row.booking_ref,
            "package_name": row.package_name or "Package",
            "destination": row.destination or "",
            "travel_date": str(row.travel_date),
            "persons": row.num_persons,
            "amount": float(row.total_amount),
            "status": row.status.value if row.status else "pending",
            "booked_at": row.created_at.isoformat() if row.created_at else None,
        })

    stmt = (
        select(
            ActivityBooking.id, ActivityBooking.booking_ref, ActivityBooking.booking_date,
            ActivityBooking.num_persons, ActivityBooking.total_amount, ActivityBooking.status,
            ActivityBooking.created_at, Activity.activity_name, Activity.destination,
        )
        .outerjoin(Activity, ActivityBooking.activity_id == Activity.activity_id)
        .where(ActivityBooking.customer_id == cid)
        .order_by(ActivityBooking.created_at.desc().nulls_last())
    )
    act_bookings = []
    for row in db.execute(stmt).all():
        act_bookings.append({
            "id": row.id,
            "ref": row.booking_ref,
            "activity_name": row.activity_name or "Activity",
            "destination": row.destination or "",
            "date": str(row.booking_date),
            "persons": row.num_persons,
            "amount": float(row.total_amount),
            "status": row.status.value if row.status else "pending",
            "booked_at": row.created_at.isoformat() if row.created_at else None,
        })

    stmt = (
        select(Review)
        .where(Review.customer_id == cid)
        .order_by(Review.created_at.desc().nulls_last())
    )
    reviews = []
    for r in db.scalars(stmt).all():
        reviews.append({
            "review_id": r.review_id,
            "entity_type": r.entity_type,
            "entity_id": r.entity_id,
            "rating": r.rating,
            "title": r.title or "",
            "comment": r.comment or "",
            "verified": r.verified_visit,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })

    guide_ids = [b[0] for b in (
        db.execute(
            select(Booking.guide_id)
            .where(Booking.customer_id == cid, Booking.guide_id.isnot(None))
            .distinct()
        ).all()
    )]
    guides = []
    if guide_ids:
        guide_stmt = select(Guide).where(Guide.guide_id.in_(guide_ids))
        for g in db.scalars(guide_stmt).all():
            guides.append({
                "guide_id": g.guide_id,
                "name": g.guide_name,
                "city": g.guide_city or "",
                "language": g.guide_language or "",
                "experience": g.guide_experience or 0,
            })

    total_spent_hotels = sum(b["amount"] for b in hotel_bookings if b["status"] in ("confirmed", "completed"))
    total_spent_packages = sum(b["amount"] for b in pkg_bookings if b["status"] in ("confirmed", "completed"))
    total_spent_activities = sum(b["amount"] for b in act_bookings if b["status"] in ("confirmed", "completed"))

    return {
        "profile": profile,
        "stats": {
            "hotel_bookings": len(hotel_bookings),
            "package_bookings": len(pkg_bookings),
            "activity_bookings": len(act_bookings),
            "reviews_written": len(reviews),
            "guides_met": len(guides),
            "total_spent": round(total_spent_hotels + total_spent_packages + total_spent_activities, 2),
        },
        "hotel_bookings": hotel_bookings,
        "package_bookings": pkg_bookings,
        "activity_bookings": act_bookings,
        "reviews": reviews,
        "guides": guides,
    }


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: DBDep, _: CurrentAdminDep):
    return CustomerService(db).get(customer_id)

@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: DBDep, _: CurrentAdminDep):
    CustomerService(db).delete(customer_id)