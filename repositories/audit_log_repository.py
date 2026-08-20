from datetime import datetime
from typing import Optional, Sequence, Tuple
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import AuditLog
from .base import GenericRepository


class AuditLogRepository(GenericRepository[AuditLog]):
    model = AuditLog

    def filter_logs(
        self,
        *,
        user_id: Optional[int] = None,
        user_role: Optional[str] = None,
        action: Optional[str] = None,
        entity_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[AuditLog]:
        stmt = select(AuditLog).order_by(AuditLog.timestamp.desc())
        
        if user_id:
            stmt = stmt.where(AuditLog.user_id == user_id)
        if user_role:
            stmt = stmt.where(AuditLog.user_role == user_role)
        if action:
            stmt = stmt.where(AuditLog.action == action)
        if entity_type:
            stmt = stmt.where(AuditLog.entity_type == entity_type)
        if start_date:
            stmt = stmt.where(AuditLog.timestamp >= start_date)
        if end_date:
            stmt = stmt.where(AuditLog.timestamp <= end_date)
            
        stmt = stmt.offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def count_filtered(self, **filters) -> int:
        stmt = select(func.count()).select_from(AuditLog)
        if filters.get("user_id"):
            stmt = stmt.where(AuditLog.user_id == filters["user_id"])
        if filters.get("user_role"):
            stmt = stmt.where(AuditLog.user_role == filters["user_role"])
        if filters.get("action"):
            stmt = stmt.where(AuditLog.action == filters["action"])
        if filters.get("entity_type"):
            stmt = stmt.where(AuditLog.entity_type == filters["entity_type"])
        if filters.get("start_date"):
            stmt = stmt.where(AuditLog.timestamp >= filters["start_date"])
        if filters.get("end_date"):
            stmt = stmt.where(AuditLog.timestamp <= filters["end_date"])
        return int(self.db.scalar(stmt) or 0)