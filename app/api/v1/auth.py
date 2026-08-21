from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...dependencies import DBDep
from ...schemas.auth import TokenResponse, RefreshTokenRequest
from ...schemas.admin import AdminCreate, AdminLogin
from ...schemas.employee import EmployeeCreate, EmployeeLogin
from ...schemas.customer import CustomerCreate, CustomerLogin
from ...services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/admin", response_model=TokenResponse, status_code=201)
def register_admin(payload: AdminCreate, db: DBDep):
    user = AuthService(db).register_admin(payload)
    return AuthService(db).login_admin(AdminLogin(
        admin_email=payload.admin_email, 
        admin_password=payload.admin_password
    ))

@router.post("/login/admin", response_model=TokenResponse)
def login_admin(payload: AdminLogin, db: DBDep):
    return AuthService(db).login_admin(payload)

@router.post("/register/employee", response_model=TokenResponse, status_code=201)
def register_employee(payload: EmployeeCreate, db: DBDep):
    AuthService(db).register_employee(payload)
    return AuthService(db).login_employee(EmployeeLogin(
        employee_email=payload.employee_email,
        employee_password=payload.employee_password
    ))

@router.post("/login/employee", response_model=TokenResponse)
def login_employee(payload: EmployeeLogin, db: DBDep):
    return AuthService(db).login_employee(payload)

@router.post("/register/customer", response_model=TokenResponse, status_code=201)
def register_customer(payload: CustomerCreate, db: DBDep):
    AuthService(db).register_customer(payload)
    return AuthService(db).login_customer(CustomerLogin(
        customer_email=payload.customer_email,
        customer_password=payload.customer_password
    ))

@router.post("/login/customer", response_model=TokenResponse)
def login_customer(payload: CustomerLogin, db: DBDep):
    return AuthService(db).login_customer(payload)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: DBDep):
    return AuthService(db).refresh_tokens(payload.refresh_token)