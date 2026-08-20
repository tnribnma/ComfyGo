from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .common import TimestampedOut


class GuideBase(BaseModel):
    guide_name: str = Field(..., min_length=2, max_length=120)
    guide_email: EmailStr
    guide_phone: Optional[str] = Field(default=None, max_length=20)
    guide_language: Optional[str] = Field(default=None, max_length=100)
    guide_experience: Optional[int] = Field(default=0, ge=0)


class GuideCreate(GuideBase):
    pass


class GuideUpdate(BaseModel):
    guide_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    guide_email: Optional[EmailStr] = None
    guide_phone: Optional[str] = Field(default=None, max_length=20)
    guide_language: Optional[str] = Field(default=None, max_length=100)
    guide_experience: Optional[int] = Field(default=None, ge=0)


class GuideOut(GuideBase, TimestampedOut):
    guide_id: int
    model_config = ConfigDict(from_attributes=True)