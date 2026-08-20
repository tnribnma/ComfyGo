from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Customer
from .base import GenericRepository


class CustomerRepository(GenericRepository[Customer]):
    model = Customer

    def get_by_email(self, email: str) -> Optional[Customer]:
        stmt = select(Customer).where(Customer.customer_email == email)
        return self.db.scalars(stmt).first()

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None