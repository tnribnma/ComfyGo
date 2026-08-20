from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from .common import TimestampedOut


class AdminBase(BaseModel):
    admin_name: str = Field(..., min_length=2, max_length=120)
    admin_email: EmailStr
    admin_phone: Optional[str] = Field(default=None, max_length=20)


class AdminCreate(AdminBase):
    admin_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("admin_password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class AdminUpdate(BaseModel):
    admin_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    admin_email: Optional[EmailStr] = None
    admin_phone: Optional[str] = Field(default=None, max_length=20)
    admin_password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class AdminLogin(BaseModel):
    admin_email: EmailStr
    admin_password: str


class AdminOut(AdminBase, TimestampedOut):
    admin_id: int
    model_config = ConfigDict(from_attributes=True)