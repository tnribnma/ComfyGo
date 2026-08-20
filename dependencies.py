from typing import Annotated, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .core.security import decode_token
from .core.exceptions import AuthenticationError, AuthorizationError
from .models import Admin, Employee, Customer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=True,
)

AuthenticatedUser = Union[Admin, Employee, Customer]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> AuthenticatedUser:
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_raw = payload.get("sub")
    role = payload.get("role")
    if not user_id_raw or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token payload",
        )

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid subject in token",
        )

    model_map = {
        "admin":    Admin,
        "employee": Employee,
        "customer": Customer,
    }
    model = model_map.get(role)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unknown role '{role}'",
        )

    user = db.get(model, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )
    return user


def _require_role(user: AuthenticatedUser, expected_type: type) -> AuthenticatedUser:
    if not isinstance(user, expected_type):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This endpoint requires {expected_type.__name__} role",
        )
    return user


def require_admin(user: Annotated[Admin, Depends(get_current_user)]) -> Admin:
    """Only Admins may pass."""
    return _require_role(user, Admin)


def require_employee(
    user: Annotated[Employee, Depends(get_current_user)]
) -> Employee:
    """Only Employees may pass."""
    return _require_role(user, Employee)


def require_customer(
    user: Annotated[Customer, Depends(get_current_user)]
) -> Customer:
    """Only Customers may pass."""
    return _require_role(user, Customer)


def get_optional_user(
    token: Annotated[str, Depends(oauth2_scheme)] = None,
    db: Annotated[Session, Depends(get_db)] = None,
) -> Union[AuthenticatedUser, None]:
    """Returns the user if a valid token is present, else None — never raises."""
    if not token:
        return None
    try:
        return get_current_user(token=token, db=db)
    except HTTPException:
        return None


DBDep = Annotated[Session, Depends(get_db)]
CurrentAdminDep = Annotated[Admin, Depends(require_admin)]
CurrentEmployeeDep = Annotated[Employee, Depends(require_employee)]
CurrentCustomerDep = Annotated[Customer, Depends(require_customer)]
CurrentUserDep = Annotated[AuthenticatedUser, Depends(get_current_user)]