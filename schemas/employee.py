from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from .common import TimestampedOut


class EmployeeBase(BaseModel):
    employee_name: str = Field(..., min_length=2, max_length=120)
    employee_email: EmailStr
    employee_phone: Optional[str] = Field(default=None, max_length=20)
    employee_position: Optional[str] = Field(default=None, max_length=100)
    hotel_id: int = Field(..., gt=0)
    admin_id: int = Field(..., gt=0)


class EmployeeCreate(EmployeeBase):
    employee_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("employee_password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class EmployeeUpdate(BaseModel):
    employee_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    employee_email: Optional[EmailStr] = None
    employee_phone: Optional[str] = Field(default=None, max_length=20)
    employee_position: Optional[str] = Field(default=None, max_length=100)
    hotel_id: Optional[int] = Field(default=None, gt=0)
    admin_id: Optional[int] = Field(default=None, gt=0)
    employee_password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class EmployeeLogin(BaseModel):
    employee_email: EmailStr
    employee_password: str


class EmployeeOut(EmployeeBase, TimestampedOut):
    employee_id: int
    model_config = ConfigDict(from_attributes=True)


class EmployeeOutNoPwd(BaseModel):
    """Public-facing employee representation (no password, no admin_id)."""
    employee_id: int
    employee_name: str
    employee_email: EmailStr
    employee_phone: Optional[str]
    employee_position: Optional[str]
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)