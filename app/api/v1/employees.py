from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.employee import EmployeeOut, EmployeeCreate, EmployeeUpdate
from ...schemas.common import PaginatedResponse
from ...services import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=PaginatedResponse[EmployeeOut])
def list_employees(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    items = EmployeeService(db).list(skip=skip, limit=limit)
    return PaginatedResponse[EmployeeOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.post("/", response_model=EmployeeOut, status_code=201)
def create_employee(payload: EmployeeCreate, db: DBDep, _: CurrentAdminDep):
    return EmployeeService(db).create(payload)

@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: DBDep, _: CurrentAdminDep):
    return EmployeeService(db).get(employee_id)

@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, payload: EmployeeUpdate, db: DBDep, _: CurrentAdminDep):
    return EmployeeService(db).update(employee_id, payload)

@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: DBDep, _: CurrentAdminDep):
    EmployeeService(db).delete(employee_id)