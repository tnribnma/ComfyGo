from sqlalchemy.orm import Session
from ..repositories import TourPackageRepository
from ..schemas.package import TourPackageCreate, TourPackageUpdate


class TourPackageService:
    def __init__(self, db: Session):
        self.repo = TourPackageRepository(db)

    def get(self, package_id: int):
        return self.repo.get_or_404(package_id)

    def search(self, destination=None, country=None, min_price=None, max_price=None,
               difficulty=None, skip=0, limit=50):
        return self.repo.search(destination=destination, country=country, min_price=min_price,
                                max_price=max_price, difficulty=difficulty, skip=skip, limit=limit)

    def create(self, payload: TourPackageCreate):
        return self.repo.create(payload.model_dump())

    def update(self, package_id: int, payload: TourPackageUpdate):
        return self.repo.update(package_id, payload.model_dump(exclude_unset=True))

    def delete(self, package_id: int) -> None:
        self.repo.delete(package_id)
