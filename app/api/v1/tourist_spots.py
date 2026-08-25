from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.tourist_spot import TouristSpotOut, TouristSpotCreate, TouristSpotUpdate
from ...schemas.common import PaginatedResponse
from ...services import TouristSpotService

router = APIRouter(prefix="/tourist-spots", tags=["Tourist Spots"])


@router.get("/", response_model=PaginatedResponse[TouristSpotOut])
def list_spots(
    db: DBDep,
    city: str = Query(None),
    country: str = Query(None),
    category: str = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    items = TouristSpotService(db).search(city=city, country=country, category=category, skip=skip, limit=limit)
    return PaginatedResponse[TouristSpotOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/destinations")
def list_spot_destinations(db: DBDep):
    """Return unique city+country combinations with spot counts."""
    from sqlalchemy import func, select
    from ...models import TouristSpot
    stmt = (
        select(
            TouristSpot.spot_city.label("city"),
            TouristSpot.spot_country.label("country"),
            func.count(TouristSpot.spot_id).label("spot_count"),
        )
        .group_by(TouristSpot.spot_city, TouristSpot.spot_country)
        .order_by(func.count(TouristSpot.spot_id).desc(), TouristSpot.spot_city)
    )
    return [dict(row) for row in db.execute(stmt).mappings().all()]


@router.post("/", response_model=TouristSpotOut, status_code=201)
def create_spot(payload: TouristSpotCreate, db: DBDep, _: CurrentAdminDep):
    return TouristSpotService(db).create(payload)


@router.get("/{spot_id}", response_model=TouristSpotOut)
def get_spot(spot_id: int, db: DBDep):
    return TouristSpotService(db).get(spot_id)


@router.put("/{spot_id}", response_model=TouristSpotOut)
def update_spot(spot_id: int, payload: TouristSpotUpdate, db: DBDep, _: CurrentAdminDep):
    return TouristSpotService(db).update(spot_id, payload)


@router.delete("/{spot_id}", status_code=204)
def delete_spot(spot_id: int, db: DBDep, _: CurrentAdminDep):
    TouristSpotService(db).delete(spot_id)
