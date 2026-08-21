from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...dependencies import CurrentAdminDep, DBDep
from ...models import Customer, Hotel, Booking, Payment, Employee, Guide, AuditLog
from ...schemas.audit_log import AuditLogOut
from ...schemas.common import PaginatedResponse
from ...repositories.audit_log_repository import AuditLogRepository

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

@router.get("/stats", summary="Get overall system statistics")
def get_system_stats(db: DBDep, _: CurrentAdminDep):
    return {
        "customers": db.query(func.count(Customer.customer_id)).scalar() or 0,
        "hotels": db.query(func.count(Hotel.hotel_id)).scalar() or 0,
        "employees": db.query(func.count(Employee.employee_id)).scalar() or 0,
        "guides": db.query(func.count(Guide.guide_id)).scalar() or 0,
        "bookings": db.query(func.count(Booking.booking_id)).scalar() or 0,
        "payments": db.query(func.count(Payment.payment_id)).scalar() or 0,
        "audit_logs": db.query(func.count(AuditLog.log_id)).scalar() or 0,
    }

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
    filters = {"user_id": user_id, "user_role": user_role, "action": action,
               "entity_type": entity_type, "start_date": start_date, "end_date": end_date}
    logs = repo.filter_logs(skip=skip, limit=page_size, **filters)
    total = repo.count_filtered(**filters)
    return PaginatedResponse[AuditLogOut](
        items=[AuditLogOut.model_validate(log) for log in logs],
        total=total, page=page, page_size=page_size, pages=(total + page_size - 1) // page_size
    )

@router.get("/recent-activity", response_model=List[AuditLogOut])
def get_recent_activity(db: DBDep, _: CurrentAdminDep, limit: int = Query(10, le=50)):
    repo = AuditLogRepository(db)
    return repo.filter_logs(skip=0, limit=limit)