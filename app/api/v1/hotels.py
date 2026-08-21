from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.hotel import HotelOut, HotelCreate, HotelUpdate
from ...schemas.common import PaginatedResponse
from ...services import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("/", response_model=PaginatedResponse[HotelOut])
def list_hotels(db: DBDep, skip: int = 0, limit: int = 100):
    items = HotelService(db).list(skip=skip, limit=limit)
    return PaginatedResponse[HotelOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.get("/search", response_model=PaginatedResponse[HotelOut])
def search_hotels(
    db: DBDep,
    city: str = None, country: str = None,
    min_rating: float = None, max_rating: float = None,
    skip: int = 0, limit: int = 50
):
    items = HotelService(db).search(city=city, country=country, min_rating=min_rating, max_rating=max_rating, skip=skip, limit=limit)
    return PaginatedResponse[HotelOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.post("/", response_model=HotelOut, status_code=201)
def create_hotel(payload: HotelCreate, db: DBDep, _: CurrentAdminDep):
    return HotelService(db).create(payload)

@router.get("/{hotel_id}", response_model=HotelOut)
def get_hotel(hotel_id: int, db: DBDep):
    return HotelService(db).get(hotel_id)

@router.put("/{hotel_id}", response_model=HotelOut)
def update_hotel(hotel_id: int, payload: HotelUpdate, db: DBDep, _: CurrentAdminDep):
    return HotelService(db).update(hotel_id, payload)

@router.delete("/{hotel_id}", status_code=204)
def delete_hotel(hotel_id: int, db: DBDep, _: CurrentAdminDep):
    HotelService(db).delete(hotel_id)