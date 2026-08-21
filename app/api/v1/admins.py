from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.admin import AdminOut, AdminCreate, AdminUpdate
from ...schemas.common import PaginatedResponse
from ...services import AdminService

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.get("/", response_model=PaginatedResponse[AdminOut])
def list_admins(db: DBDep, _: CurrentAdminDep, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * page_size
    items = AdminService(db).list(skip=skip, limit=page_size)
    return PaginatedResponse[AdminOut](items=items, total=len(items), page=page, page_size=page_size, pages=1)

@router.post("/", response_model=AdminOut, status_code=201)
def create_admin(payload: AdminCreate, db: DBDep, _: CurrentAdminDep):
    return AdminService(db).create(payload)

@router.get("/{admin_id}", response_model=AdminOut)
def get_admin(admin_id: int, db: DBDep, _: CurrentAdminDep):
    return AdminService(db).get(admin_id)

@router.put("/{admin_id}", response_model=AdminOut)
def update_admin(admin_id: int, payload: AdminUpdate, db: DBDep, _: CurrentAdminDep):
    return AdminService(db).update(admin_id, payload)

@router.delete("/{admin_id}", status_code=204)
def delete_admin(admin_id: int, db: DBDep, _: CurrentAdminDep):
    AdminService(db).delete(admin_id)