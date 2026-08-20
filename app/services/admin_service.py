from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..repositories import AdminRepository
from ..schemas.admin import AdminCreate, AdminUpdate


class AdminService:
    def __init__(self, db: Session):
        self.repo = AdminRepository(db)

    def get(self, admin_id: int):
        return self.repo.get_or_404(admin_id)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(skip=skip, limit=limit)

    def create(self, payload: AdminCreate):
        data = payload.model_dump()
        data["admin_password"] = get_password_hash(data["admin_password"])
        return self.repo.create(data)

    def update(self, admin_id: int, payload: AdminUpdate):
        data = payload.model_dump(exclude_unset=True)
        if "admin_password" in data and data["admin_password"]:
            data["admin_password"] = get_password_hash(data["admin_password"])
        return self.repo.update(admin_id, data)

    def delete(self, admin_id: int) -> None:
        self.repo.delete(admin_id)