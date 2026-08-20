from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Admin
from .base import GenericRepository


class AdminRepository(GenericRepository[Admin]):
    model = Admin

    def get_by_email(self, email: str) -> Optional[Admin]:
        stmt = select(Admin).where(Admin.admin_email == email)
        return self.db.scalars(stmt).first()

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None
