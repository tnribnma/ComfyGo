from typing import Optional
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


@router.get("/search", response_model=PaginatedResponse[GuideOut])
def search_guides(
    db: DBDep,
    city: Optional[str] = None,
    language: Optional[str] = None,
    min_experience: Optional[int] = None,
    is_available: Optional[bool] = None,
    min_rate: Optional[float] = None,
    max_rate: Optional[float] = None,
    specialty: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="experience, price_asc, price_desc, rating, name"),
    skip: int = 0,
    limit: int = 50,
):
    items = GuideService(db).search(
        city=city, language=language, min_experience=min_experience,
        is_available=is_available, min_rate=min_rate, max_rate=max_rate,
        specialty=specialty, sort_by=sort_by, skip=skip, limit=limit,
    )
    return PaginatedResponse[GuideOut](items=items, total=len(items), page=1, page_size=limit, pages=1)


@router.get("/by-city", response_model=list[GuideOut])
def guides_by_city(db: DBDep, city: str = Query(...)):
    """Return guides who operate in a specific city."""
    from ...repositories import GuideRepository
    repo = GuideRepository(db)
    return repo.list_by_city(city)


@router.get("/filter-options")
def filter_options(db: DBDep):
    """Return available cities, languages and specialties for filter dropdowns."""
    svc = GuideService(db)
    return {
        "cities": svc.list_cities(),
        "languages": svc.list_languages(),
    }


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