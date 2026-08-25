from datetime import datetime, date, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case, select

from ...dependencies import CurrentAdminDep, DBDep
from ...models import (
    Customer, Hotel, Booking, Payment, Employee, Guide, AuditLog,
    PackageBooking, ActivityBooking, Review, Restaurant,
)
from ...schemas.audit_log import AuditLogOut
from ...schemas.common import PaginatedResponse
from ...repositories.audit_log_repository import AuditLogRepository

router = APIRouter(prefix="/admin", tags=["Admin Panel"])


@router.get("/stats", summary="Get overall system statistics")
def get_system_stats(db: DBDep, _: CurrentAdminDep):
    today_start = datetime.combine(date.today(), datetime.min.time())

    total_customers = db.query(func.count(Customer.customer_id)).scalar() or 0
    total_hotels = db.query(func.count(Hotel.hotel_id)).scalar() or 0
    total_employees = db.query(func.count(Employee.employee_id)).scalar() or 0
    total_guides = db.query(func.count(Guide.guide_id)).scalar() or 0
    total_bookings = db.query(func.count(Booking.booking_id)).scalar() or 0
    total_payments = db.query(func.count(Payment.payment_id)).scalar() or 0
    total_reviews = db.query(func.count(Review.review_id)).scalar() or 0
    total_restaurants = db.query(func.count(Restaurant.restaurant_id)).scalar() or 0
    total_pkg_bookings = db.query(func.count(PackageBooking.id)).scalar() or 0
    total_act_bookings = db.query(func.count(ActivityBooking.id)).scalar() or 0

    total_revenue = db.query(func.coalesce(func.sum(Payment.payment_amount), 0.0)).filter(
        Payment.payment_status.in_(["success", "completed"])
    ).scalar() or 0.0

    pkg_revenue = db.query(func.coalesce(func.sum(PackageBooking.total_amount), 0.0)).filter(
        PackageBooking.status.in_(["confirmed", "completed"])
    ).scalar() or 0.0

    act_revenue = db.query(func.coalesce(func.sum(ActivityBooking.total_amount), 0.0)).filter(
        ActivityBooking.status.in_(["confirmed", "completed"])
    ).scalar() or 0.0

    grand_total_revenue = float(total_revenue) + float(pkg_revenue) + float(act_revenue)

    today_bookings = db.query(func.count(Booking.booking_id)).filter(
        Booking.created_at >= today_start
    ).scalar() or 0
    today_payments = db.query(func.count(Payment.payment_id)).filter(
        Payment.payment_date >= today_start
    ).scalar() or 0
    today_revenue = db.query(func.coalesce(func.sum(Payment.payment_amount), 0.0)).filter(
        Payment.payment_status.in_(["success", "completed"]),
        Payment.payment_date >= today_start,
    ).scalar() or 0.0
    today_new_customers = db.query(func.count(Customer.customer_id)).filter(
        Customer.created_at >= today_start
    ).scalar() or 0
    today_pkg_bookings = db.query(func.count(PackageBooking.id)).filter(
        PackageBooking.created_at >= today_start
    ).scalar() or 0
    today_act_bookings = db.query(func.count(ActivityBooking.id)).filter(
        ActivityBooking.created_at >= today_start
    ).scalar() or 0
    today_reviews = db.query(func.count(Review.review_id)).filter(
        Review.created_at >= today_start
    ).scalar() or 0

    booking_status_counts = db.query(
        Booking.booking_status, func.count(Booking.booking_id)
    ).group_by(Booking.booking_status).all()
    status_breakdown = {
        status.value if hasattr(status, "value") else str(status): count
        for status, count in booking_status_counts
    }

    recent_actions = db.query(
        AuditLog.action, func.count(AuditLog.log_id)
    ).filter(
        AuditLog.timestamp >= today_start - timedelta(hours=24)
    ).group_by(AuditLog.action).all()
    action_breakdown = {
        action if isinstance(action, str) else str(action): count
        for action, count in recent_actions
    }

    top_reviewed = db.query(
        Review.entity_type, func.count(Review.review_id), func.avg(Review.rating)
    ).group_by(Review.entity_type).all()
    review_summary = {
        etype: {"count": cnt, "avg_rating": round(float(avg), 1) if avg else 0}
        for etype, cnt, avg in top_reviewed
    }

    return {
        "customers": total_customers,
        "hotels": total_hotels,
        "employees": total_employees,
        "guides": total_guides,
        "bookings": total_bookings,
        "payments": total_payments,
        "reviews": total_reviews,
        "restaurants": total_restaurants,
        "package_bookings": total_pkg_bookings,
        "activity_bookings": total_act_bookings,
        "total_revenue": round(grand_total_revenue, 2),
        "hotel_revenue": round(float(total_revenue), 2),
        "package_revenue": round(float(pkg_revenue), 2),
        "activity_revenue": round(float(act_revenue), 2),
        "today_bookings": today_bookings,
        "today_payments": today_payments,
        "today_revenue": round(float(today_revenue), 2),
        "today_new_customers": today_new_customers,
        "today_pkg_bookings": today_pkg_bookings,
        "today_act_bookings": today_act_bookings,
        "today_reviews": today_reviews,
        "booking_status": status_breakdown,
        "recent_actions": action_breakdown,
        "review_summary": review_summary,
    }

@router.get("/bookings/enriched")
def list_bookings_enriched(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    stmt = (
        select(
            Booking, Customer.customer_name, Customer.customer_email,
            Hotel.hotel_name, Hotel.hotel_city, Guide.guide_name,
        )
        .outerjoin(Customer, Booking.customer_id == Customer.customer_id)
        .outerjoin(Hotel, Booking.hotel_id == Hotel.hotel_id)
        .outerjoin(Guide, Booking.guide_id == Guide.guide_id)
        .order_by(Booking.created_at.desc().nulls_last(), Booking.booking_id.desc())
        .offset(skip).limit(limit)
    )
    rows = db.execute(stmt).all()
    items = []
    for b, cust_name, cust_email, hotel_name, hotel_city, guide_name in rows:
        items.append({
            "booking_id": b.booking_id,
            "customer_id": b.customer_id,
            "customer_name": cust_name or f"Customer #{b.customer_id}",
            "customer_email": cust_email or "",
            "hotel_id": b.hotel_id,
            "hotel_name": hotel_name or f"Hotel #{b.hotel_id}",
            "hotel_city": hotel_city or "",
            "guide_name": guide_name or None,
            "check_in_date": str(b.check_in_date),
            "check_out_date": str(b.check_out_date),
            "number_of_guests": b.number_of_guests,
            "total_amount": float(b.total_amount),
            "booking_status": b.booking_status.value if b.booking_status else "pending",
            "booking_date": str(b.booking_date) if b.booking_date else None,
            "created_at": b.created_at.isoformat() if b.created_at else None,
        })
    return items


@router.get("/package-bookings/enriched")
def list_package_bookings_enriched(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    from ...models import TourPackage
    stmt = (
        select(
            PackageBooking, Customer.customer_name, Customer.customer_email,
            TourPackage.package_name, TourPackage.destination, TourPackage.price_per_person,
        )
        .outerjoin(Customer, PackageBooking.customer_id == Customer.customer_id)
        .outerjoin(TourPackage, PackageBooking.package_id == TourPackage.package_id)
        .order_by(PackageBooking.created_at.desc().nulls_last(), PackageBooking.id.desc())
        .offset(skip).limit(limit)
    )
    rows = db.execute(stmt).all()
    items = []
    for pb, cust_name, cust_email, pkg_name, dest, price_pp in rows:
        items.append({
            "id": pb.id,
            "booking_ref": pb.booking_ref,
            "customer_id": pb.customer_id,
            "customer_name": cust_name or f"Customer #{pb.customer_id}",
            "customer_email": cust_email or "",
            "package_id": pb.package_id,
            "package_name": pkg_name or f"Package #{pb.package_id}",
            "destination": dest or "",
            "travel_date": str(pb.travel_date),
            "num_persons": pb.num_persons,
            "total_amount": float(pb.total_amount),
            "status": pb.status.value if pb.status else "pending",
            "contact_name": pb.contact_name or "",
            "contact_email": pb.contact_email or "",
            "special_requests": pb.special_requests or "",
            "created_at": pb.created_at.isoformat() if pb.created_at else None,
        })
    return items

@router.get("/activity-bookings/enriched")
def list_activity_bookings_enriched(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    from ...models import Activity
    stmt = (
        select(
            ActivityBooking, Customer.customer_name, Customer.customer_email,
            Activity.activity_name, Activity.destination, Activity.price,
        )
        .outerjoin(Customer, ActivityBooking.customer_id == Customer.customer_id)
        .outerjoin(Activity, ActivityBooking.activity_id == Activity.activity_id)
        .order_by(ActivityBooking.created_at.desc().nulls_last(), ActivityBooking.id.desc())
        .offset(skip).limit(limit)
    )
    rows = db.execute(stmt).all()
    items = []
    for ab, cust_name, cust_email, act_name, dest, price in rows:
        items.append({
            "id": ab.id,
            "booking_ref": ab.booking_ref,
            "customer_id": ab.customer_id,
            "customer_name": cust_name or f"Customer #{ab.customer_id}",
            "customer_email": cust_email or "",
            "activity_id": ab.activity_id,
            "activity_name": act_name or f"Activity #{ab.activity_id}",
            "destination": dest or "",
            "booking_date": str(ab.booking_date),
            "num_persons": ab.num_persons,
            "total_amount": float(ab.total_amount),
            "status": ab.status.value if ab.status else "pending",
            "contact_name": ab.contact_name or "",
            "contact_email": ab.contact_email or "",
            "special_requests": ab.special_requests or "",
            "created_at": ab.created_at.isoformat() if ab.created_at else None,
        })
    return items


@router.get("/reviews/enriched")
def list_reviews_enriched(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    stmt = (
        select(
            Review, Customer.customer_name, Customer.customer_email,
        )
        .outerjoin(Customer, Review.customer_id == Customer.customer_id)
        .order_by(Review.created_at.desc().nulls_last(), Review.review_id.desc())
        .offset(skip).limit(limit)
    )
    rows = db.execute(stmt).all()
    items = []
    for r, cust_name, cust_email in rows:
        items.append({
            "review_id": r.review_id,
            "customer_id": r.customer_id,
            "customer_name": cust_name or f"Customer #{r.customer_id}",
            "customer_email": cust_email or "",
            "entity_type": r.entity_type,
            "entity_id": r.entity_id,
            "rating": r.rating,
            "title": r.title or "",
            "comment": r.comment or "",
            "verified_visit": r.verified_visit,
            "helpful_count": r.helpful_count,
            "owner_response": r.owner_response or "",
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })
    return items


@router.get("/restaurants")
def list_all_restaurants(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    from ...repositories import RestaurantRepository
    repo = RestaurantRepository(db)
    items = repo.get_multi(skip=skip, limit=limit)
    return [
        {
            "restaurant_id": r.restaurant_id,
            "restaurant_name": r.restaurant_name,
            "destination": r.destination,
            "country": r.country,
            "cuisine": r.cuisine,
            "rating": float(r.rating) if r.rating else None,
            "price_range": r.price_range,
            "is_featured": r.is_featured,
            "vegetarian_options": r.vegetarian_options,
            "outdoor_seating": r.outdoor_seating,
            "delivery_available": r.delivery_available,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in items
    ]

@router.get("/audit-logs", response_model=PaginatedResponse[AuditLogOut])
def get_audit_logs(
    db: DBDep, _: CurrentAdminDep,
    user_id: Optional[int] = Query(None),
    user_role: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200),
):
    skip = (page - 1) * page_size
    repo = AuditLogRepository(db)
    filters = {
        "user_id": user_id, "user_role": user_role, "action": action,
        "entity_type": entity_type, "start_date": start_date, "end_date": end_date,
    }
    logs = repo.filter_logs(skip=skip, limit=page_size, **filters)
    total = repo.count_filtered(**filters)
    return PaginatedResponse[AuditLogOut](
        items=[AuditLogOut.model_validate(log) for log in logs],
        total=total, page=page, page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/recent-activity", response_model=List[AuditLogOut])
def get_recent_activity(db: DBDep, _: CurrentAdminDep, limit: int = Query(10, le=50)):
    repo = AuditLogRepository(db)
    return repo.filter_logs(skip=0, limit=limit)
