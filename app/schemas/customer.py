from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from .common import TimestampedOut


class CustomerBase(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=120)
    customer_email: EmailStr
    customer_phone: Optional[str] = Field(default=None, max_length=20)
    customer_address: Optional[str] = Field(default=None, max_length=500)


class CustomerCreate(CustomerBase):
    customer_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("customer_password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = Field(default=None, max_length=20)
    customer_address: Optional[str] = Field(default=None, max_length=500)
    customer_password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class CustomerLogin(BaseModel):
    customer_email: EmailStr
    customer_password: str


class CustomerOut(CustomerBase, TimestampedOut):
    customer_id: int
    model_config = ConfigDict(from_attributes=True)