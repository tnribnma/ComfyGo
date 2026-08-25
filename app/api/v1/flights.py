from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.flight import FlightOut, FlightCreate, FlightUpdate, FlightBookSeat
from ...schemas.common import PaginatedResponse
from ...services import FlightService

router = APIRouter(prefix="/flights", tags=["Flights"])


@router.get("/", response_model=PaginatedResponse[FlightOut])
def list_flights(
    db: DBDep,
    departure_city: str = Query(None),
    arrival_city: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    items = FlightService(db).search(
        departure_city=departure_city, arrival_city=arrival_city,
        min_price=min_price, max_price=max_price, skip=skip, limit=limit
    )
    return PaginatedResponse[FlightOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/{flight_id}", response_model=FlightOut)
def get_flight(flight_id: int, db: DBDep):
    return FlightService(db).get(flight_id)


@router.post("/{flight_id}/book", summary="Book seats on a flight")
def book_flight_seats(flight_id: int, payload: FlightBookSeat, db: DBDep):
    return FlightService(db).book_seats(flight_id, payload)


@router.post("/", response_model=FlightOut, status_code=201)
def create_flight(payload: FlightCreate, db: DBDep, _: CurrentAdminDep):
    return FlightService(db).create(payload)


@router.put("/{flight_id}", response_model=FlightOut)
def update_flight(flight_id: int, payload: FlightUpdate, db: DBDep, _: CurrentAdminDep):
    return FlightService(db).update(flight_id, payload)


@router.delete("/{flight_id}", status_code=204)
def delete_flight(flight_id: int, db: DBDep, _: CurrentAdminDep):
    FlightService(db).delete(flight_id)
