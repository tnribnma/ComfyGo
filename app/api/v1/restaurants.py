from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.restaurant import RestaurantOut, RestaurantCreate, RestaurantUpdate
from ...schemas.common import PaginatedResponse
from ...services import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/", response_model=PaginatedResponse[RestaurantOut])
def list_restaurants(
    db: DBDep,
    destination: str = Query(None),
    cuisine: str = Query(None),
    min_rating: float = Query(None),
    price_range: str = Query(None, description="Filter by price: $, $$, $$$, $$$$"),
    vegetarian: bool = Query(None, description="Vegetarian-friendly only"),
    outdoor: bool = Query(None, description="Outdoor seating only"),
    delivery: bool = Query(None, description="Delivery available only"),
    reservations: bool = Query(None, description="Accepts reservations"),
    wifi: bool = Query(None, description="Free wifi available"),
    featured: bool = Query(None, description="Featured restaurants only"),
    skip: int = 0,
    limit: int = 100,
):
    items = RestaurantService(db).search(
        destination=destination, cuisine=cuisine, min_rating=min_rating,
        price_range=price_range, vegetarian=vegetarian, outdoor=outdoor,
        delivery=delivery, reservations=reservations, wifi=wifi,
        featured=featured, skip=skip, limit=limit,
    )
    return PaginatedResponse[RestaurantOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/cuisines", response_model=list[str])
def list_cuisines(db: DBDep):
    """Return distinct cuisine types available."""
    return RestaurantService(db).distinct_cuisines()


@router.get("/destinations", response_model=list[str])
def list_restaurant_destinations(db: DBDep):
    """Return distinct destinations with restaurants."""
    return RestaurantService(db).distinct_destinations()


@router.get("/top", response_model=PaginatedResponse[RestaurantOut])
def top_restaurants(db: DBDep, limit: int = 10):
    """Return top-rated restaurants."""
    items = RestaurantService(db).top_restaurants(limit=limit)
    return PaginatedResponse[RestaurantOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: DBDep):
    return RestaurantService(db).get(restaurant_id)


@router.post("/", response_model=RestaurantOut, status_code=201)
def create_restaurant(payload: RestaurantCreate, db: DBDep, _: CurrentAdminDep):
    return RestaurantService(db).create(payload)


@router.put("/{restaurant_id}", response_model=RestaurantOut)
def update_restaurant(restaurant_id: int, payload: RestaurantUpdate, db: DBDep, _: CurrentAdminDep):
    return RestaurantService(db).update(restaurant_id, payload)


@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: int, db: DBDep, _: CurrentAdminDep):
    RestaurantService(db).delete(restaurant_id)
