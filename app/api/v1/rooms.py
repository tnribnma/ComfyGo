from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.room import RoomOut, RoomCreate, RoomUpdate
from ...schemas.common import PaginatedResponse
from ...services import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=PaginatedResponse[RoomOut])
def list_rooms(db: DBDep, hotel_id: int = Query(None), skip: int = 0, limit: int = 100):
    if hotel_id:
        items = RoomService(db).list_by_hotel(hotel_id, skip=skip, limit=limit)
    else:
        items = RoomService(db).search(skip=skip, limit=limit)
    return PaginatedResponse[RoomOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: DBDep):
    return RoomService(db).get(room_id)


@router.post("/", response_model=RoomOut, status_code=201)
def create_room(payload: RoomCreate, db: DBDep, _: CurrentAdminDep):
    return RoomService(db).create(payload)


@router.put("/{room_id}", response_model=RoomOut)
def update_room(room_id: int, payload: RoomUpdate, db: DBDep, _: CurrentAdminDep):
    return RoomService(db).update(room_id, payload)


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, db: DBDep, _: CurrentAdminDep):
    RoomService(db).delete(room_id)
