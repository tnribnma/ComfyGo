from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.promotion import PromotionOut, PromotionCreate
from ...schemas.common import PaginatedResponse
from ...services import PromotionService

router = APIRouter(prefix="/promotions", tags=["Promotions"])


@router.get("/", response_model=PaginatedResponse[PromotionOut])
def list_promotions(db: DBDep, skip: int = 0, limit: int = 100):
    items = PromotionService(db).list_active(skip=skip, limit=limit)
    return PaginatedResponse[PromotionOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/{promotion_id}", response_model=PromotionOut)
def get_promotion(promotion_id: int, db: DBDep):
    return PromotionService(db).get(promotion_id)


@router.post("/", response_model=PromotionOut, status_code=201)
def create_promotion(payload: PromotionCreate, db: DBDep, _: CurrentAdminDep):
    return PromotionService(db).create(payload)
