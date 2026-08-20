from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..core.exceptions import ConflictError
from ..repositories import CustomerRepository
from ..schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.repo = CustomerRepository(db)

    def get(self, customer_id: int):
        return self.repo.get_or_404(customer_id)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(skip=skip, limit=limit)

    def create(self, payload: CustomerCreate):
        if self.repo.email_exists(payload.customer_email):
            raise ConflictError("Email already registered")
        data = payload.model_dump()
        data["customer_password"] = get_password_hash(data["customer_password"])
        return self.repo.create(data)

    def update(self, customer_id: int, payload: CustomerUpdate):
        data = payload.model_dump(exclude_unset=True)
        if "customer_password" in data and data["customer_password"]:
            data["customer_password"] = get_password_hash(data["customer_password"])
        return self.repo.update(customer_id, data)

    def delete(self, customer_id: int) -> None:
        self.repo.delete(customer_id)