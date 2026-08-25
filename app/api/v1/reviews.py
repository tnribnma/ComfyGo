from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentCustomerDep
from ...schemas.review import ReviewOut, ReviewCreate
from ...schemas.common import PaginatedResponse
from ...services import ReviewService

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", response_model=PaginatedResponse[ReviewOut])
def list_reviews(
    db: DBDep,
    entity_type: str = Query(None),
    entity_id: int = Query(None),
    customer_id: int = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    svc = ReviewService(db)
    if entity_type and entity_id:
        items = svc.list_by_entity(entity_type, entity_id, skip=skip, limit=limit)
    elif customer_id:
        items = svc.list_by_customer(customer_id, skip=skip, limit=limit)
    else:
        items = []
    return PaginatedResponse[ReviewOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/stats")
def review_stats(db: DBDep, entity_type: str = Query(...), entity_id: int = Query(...)):
    return ReviewService(db).get_stats(entity_type, entity_id)


@router.post("/", response_model=ReviewOut, status_code=201)
def create_review(payload: ReviewCreate, db: DBDep, user: CurrentCustomerDep):
    return ReviewService(db).create(user.customer_id, payload)
