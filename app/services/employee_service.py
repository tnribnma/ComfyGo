from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..core.exceptions import NotFoundError, ConflictError
from ..repositories import EmployeeRepository, HotelRepository, AdminRepository
from ..schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EmployeeRepository(db)
        self.hotel_repo = HotelRepository(db)
        self.admin_repo = AdminRepository(db)

    def get(self, employee_id: int):
        return self.repo.get_or_404(employee_id)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(skip=skip, limit=limit)

    def list_by_hotel(self, hotel_id: int, skip: int = 0, limit: int = 100):
        if not self.hotel_repo.exists(hotel_id):
            raise NotFoundError("Hotel not found", detail=f"hotel_id={hotel_id}")
        return self.repo.list_by_hotel(hotel_id, skip=skip, limit=limit)

    def list_by_admin(self, admin_id: int, skip: int = 0, limit: int = 100):
        if not self.admin_repo.exists(admin_id):
            raise NotFoundError("Admin not found", detail=f"admin_id={admin_id}")
        return self.repo.list_by_admin(admin_id, skip=skip, limit=limit)

    def create(self, payload: EmployeeCreate):
        if not self.hotel_repo.exists(payload.hotel_id):
            raise ConflictError("Hotel does not exist", detail=f"hotel_id={payload.hotel_id}")
        if not self.admin_repo.exists(payload.admin_id):
            raise ConflictError("Admin does not exist", detail=f"admin_id={payload.admin_id}")
        if self.repo.get_by_email(payload.employee_email):
            raise ConflictError("Email already registered")

        data = payload.model_dump()
        data["employee_password"] = get_password_hash(data["employee_password"])
        return self.repo.create(data)

    def update(self, employee_id: int, payload: EmployeeUpdate):
        data = payload.model_dump(exclude_unset=True)
        if "employee_password" in data and data["employee_password"]:
            data["employee_password"] = get_password_hash(data["employee_password"])
        if "hotel_id" in data and not self.hotel_repo.exists(data["hotel_id"]):
            raise ConflictError("Hotel does not exist")
        if "admin_id" in data and not self.admin_repo.exists(data["admin_id"]):
            raise ConflictError("Admin does not exist")
        return self.repo.update(employee_id, data)

    def delete(self, employee_id: int) -> None:
        self.repo.delete(employee_id)