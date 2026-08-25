from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.local_transport import LocalTransportOut, LocalTransportCreate, LocalTransportUpdate, LocalTransportBook
from ...schemas.common import PaginatedResponse
from ...services import LocalTransportService

router = APIRouter(prefix="/local-transport", tags=["Local Transportation"])


@router.get("/", response_model=PaginatedResponse[LocalTransportOut])
def list_transport(
    db: DBDep,
    transport_type: str = Query(None, description="Bus, Train, Taxi, or Car Rental"),
    departure_city: str = Query(None),
    arrival_city: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    items = LocalTransportService(db).search(
        transport_type=transport_type, departure_city=departure_city,
        arrival_city=arrival_city, min_price=min_price, max_price=max_price,
        skip=skip, limit=limit
    )
    return PaginatedResponse[LocalTransportOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/{transport_id}", response_model=LocalTransportOut)
def get_transport(transport_id: int, db: DBDep):
    return LocalTransportService(db).get(transport_id)


@router.post("/{transport_id}/book", summary="Book seats on local transport")
def book_transport(transport_id: int, payload: LocalTransportBook, db: DBDep):
    return LocalTransportService(db).book_seats(transport_id, payload)


@router.post("/", response_model=LocalTransportOut, status_code=201)
def create_transport(payload: LocalTransportCreate, db: DBDep, _: CurrentAdminDep):
    return LocalTransportService(db).create(payload)


@router.put("/{transport_id}", response_model=LocalTransportOut)
def update_transport(transport_id: int, payload: LocalTransportUpdate, db: DBDep, _: CurrentAdminDep):
    return LocalTransportService(db).update(transport_id, payload)


@router.delete("/{transport_id}", status_code=204)
def delete_transport(transport_id: int, db: DBDep, _: CurrentAdminDep):
    LocalTransportService(db).delete(transport_id)
