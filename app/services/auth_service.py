from sqlalchemy.orm import Session

from ..core.security import (
    get_password_hash, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from ..core.exceptions import AuthenticationError, ConflictError
from ..repositories import AdminRepository, EmployeeRepository, CustomerRepository
from ..schemas.admin import AdminCreate, AdminLogin
from ..schemas.employee import EmployeeCreate, EmployeeLogin
from ..schemas.customer import CustomerCreate, CustomerLogin
from ..schemas.auth import TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.admin_repo = AdminRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.customer_repo = CustomerRepository(db)

  
    def register_admin(self, payload: AdminCreate):
        if self.admin_repo.email_exists(payload.admin_email):
            raise ConflictError("Email already registered", detail=payload.admin_email)
        data = payload.model_dump()
        data["admin_password"] = get_password_hash(data["admin_password"])
        return self.admin_repo.create(data)

    def login_admin(self, payload: AdminLogin) -> TokenResponse:
        admin = self.admin_repo.get_by_email(payload.admin_email)
        if not admin or not verify_password(payload.admin_password, admin.admin_password):
            raise AuthenticationError("Invalid email or password")
        return self._issue_tokens(user_id=admin.admin_id, role="admin")

    def register_employee(self, payload: EmployeeCreate):
        if self.employee_repo.get_by_email(payload.employee_email):
            raise ConflictError("Email already registered")
        from ..repositories import HotelRepository
        if not HotelRepository(self.db).exists(payload.hotel_id):
            raise ConflictError("Hotel does not exist", detail=f"hotel_id={payload.hotel_id}")
        if not self.admin_repo.exists(payload.admin_id):
            raise ConflictError("Admin does not exist", detail=f"admin_id={payload.admin_id}")

        data = payload.model_dump()
        data["employee_password"] = get_password_hash(data["employee_password"])
        return self.employee_repo.create(data)

    def login_employee(self, payload: EmployeeLogin) -> TokenResponse:
        emp = self.employee_repo.get_by_email(payload.employee_email)
        if not emp or not verify_password(payload.employee_password, emp.employee_password):
            raise AuthenticationError("Invalid email or password")
        return self._issue_tokens(user_id=emp.employee_id, role="employee")

 
    def register_customer(self, payload: CustomerCreate):
        if self.customer_repo.email_exists(payload.customer_email):
            raise ConflictError("Email already registered")
        data = payload.model_dump()
        data["customer_password"] = get_password_hash(data["customer_password"])
        return self.customer_repo.create(data)

    def login_customer(self, payload: CustomerLogin) -> TokenResponse:
        cust = self.customer_repo.get_by_email(payload.customer_email)
        if not cust or not verify_password(payload.customer_password, cust.customer_password):
            raise AuthenticationError("Invalid email or password")
        return self._issue_tokens(user_id=cust.customer_id, role="customer")

    def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Invalid refresh token")
        return self._issue_tokens(
            user_id=int(payload["sub"]),
            role=payload["role"],
        )

    @staticmethod
    def _issue_tokens(user_id: int, role: str) -> TokenResponse:
        return TokenResponse(
            access_token=create_access_token(subject=str(user_id), role=role),
            refresh_token=create_refresh_token(subject=str(user_id), role=role),
            role=role,
            user_id=user_id,
        )