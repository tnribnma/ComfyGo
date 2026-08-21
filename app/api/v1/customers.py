from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep, CurrentCustomerDep
from ...schemas.customer import CustomerOut, CustomerCreate, CustomerUpdate
from ...schemas.common import PaginatedResponse
from ...services import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=PaginatedResponse[CustomerOut])
def list_customers(db: DBDep, _: CurrentAdminDep, skip: int = 0, limit: int = 100):
    items = CustomerService(db).list(skip=skip, limit=limit)
    return PaginatedResponse[CustomerOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(payload: CustomerCreate, db: DBDep):
    return CustomerService(db).create(payload)

@router.get("/me", response_model=CustomerOut)
def get_my_profile(user: CurrentCustomerDep):
    return user

@router.put("/me", response_model=CustomerOut)
def update_my_profile(payload: CustomerUpdate, db: DBDep, user: CurrentCustomerDep):
    return CustomerService(db).update(user.customer_id, payload)

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: DBDep, _: CurrentAdminDep):
    return CustomerService(db).get(customer_id)

@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: DBDep, _: CurrentAdminDep):
    CustomerService(db).delete(customer_id)