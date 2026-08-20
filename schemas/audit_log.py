from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field

from .common import TimestampedOut

class AuditLogOut(BaseModel):
    log_id: int
    user_id: Optional[int]
    user_role: Optional[str]
    action: str
    entity_type: Optional[str]
    entity_id: Optional[int]
    details: Optional[dict[str, Any]]
    request_method: str
    request_path: str
    status_code: Optional[int]
    ip_address: Optional[str]
    user_agent: Optional[str]
    duration_ms: Optional[float]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogFilter(BaseModel):
    user_id: Optional[int] = None
    user_role: Optional[str] = None
    action: Optional[str] = None
    entity_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)