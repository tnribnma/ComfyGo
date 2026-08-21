from fastapi import APIRouter, Query
from ...dependencies import DBDep, CurrentAdminDep
from ...schemas.guide import GuideOut, GuideCreate, GuideUpdate
from ...schemas.common import PaginatedResponse
from ...services import GuideService

router = APIRouter(prefix="/guides", tags=["Guides"])

@router.get("/", response_model=PaginatedResponse[GuideOut])
def list_guides(db: DBDep, skip: int = 0, limit: int = 100):
    items = GuideService(db).list(skip=skip, limit=limit)
    return PaginatedResponse[GuideOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.get("/top", response_model=PaginatedResponse[GuideOut])
def top_guides(db: DBDep, limit: int = 10):
    items = GuideService(db).top_guides(limit=limit)
    return PaginatedResponse[GuideOut](items=items, total=len(items), page=1, page_size=limit, pages=1)

@router.post("/", response_model=GuideOut, status_code=201)
def create_guide(payload: GuideCreate, db: DBDep, _: CurrentAdminDep):
    return GuideService(db).create(payload)

@router.get("/{guide_id}", response_model=GuideOut)
def get_guide(guide_id: int, db: DBDep):
    return GuideService(db).get(guide_id)

@router.put("/{guide_id}", response_model=GuideOut)
def update_guide(guide_id: int, payload: GuideUpdate, db: DBDep, _: CurrentAdminDep):
    return GuideService(db).update(guide_id, payload)

@router.delete("/{guide_id}", status_code=204)
def delete_guide(guide_id: int, db: DBDep, _: CurrentAdminDep):
    GuideService(db).delete(guide_id)