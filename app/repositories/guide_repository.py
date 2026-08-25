from typing import Optional, Sequence
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from ..models import Guide
from .base import GenericRepository


class GuideRepository(GenericRepository[Guide]):
    model = Guide

    def get_by_email(self, email: str):
        stmt = select(Guide).where(Guide.guide_email == email)
        return self.db.scalars(stmt).first()

    def list_by_city(self, city: str, skip: int = 0, limit: int = 100) -> Sequence[Guide]:
        stmt = (
            select(Guide)
            .where(
                or_(
                    Guide.guide_city.ilike(f"%{city}%"),
                    Guide.regions.ilike(f"%{city}%"),
                )
            )
            .order_by(Guide.guide_experience.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_language(self, language: str, skip: int = 0, limit: int = 100) -> Sequence[Guide]:
        stmt = (
            select(Guide)
            .where(Guide.guide_language.ilike(f"%{language}%"))
            .order_by(Guide.guide_experience.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def list_by_experience_min(self, years: int, skip: int = 0, limit: int = 100) -> Sequence[Guide]:
        stmt = (
            select(Guide)
            .where(Guide.guide_experience >= years)
            .order_by(Guide.guide_experience.desc())
            .offset(skip).limit(limit)
        )
        return self.db.scalars(stmt).all()

    def top_rated(self, limit: int = 10) -> Sequence[Guide]:
        stmt = (
            select(Guide)
            .order_by(Guide.guide_experience.desc())
            .limit(limit)
        )
        return self.db.scalars(stmt).all()

    def search(
        self,
        *,
        city: Optional[str] = None,
        language: Optional[str] = None,
        min_experience: Optional[int] = None,
        is_available: Optional[bool] = None,
        min_rate: Optional[float] = None,
        max_rate: Optional[float] = None,
        specialty: Optional[str] = None,
        sort_by: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Guide]:
        stmt = select(Guide)

        if city:
            stmt = stmt.where(
                or_(
                    Guide.guide_city.ilike(f"%{city}%"),
                    Guide.regions.ilike(f"%{city}%"),
                )
            )
        if language:
            stmt = stmt.where(Guide.guide_language.ilike(f"%{language}%"))
        if min_experience is not None:
            stmt = stmt.where(Guide.guide_experience >= min_experience)
        if is_available is not None:
            stmt = stmt.where(Guide.is_available == is_available)
        if min_rate is not None:
            stmt = stmt.where(Guide.hourly_rate >= min_rate)
        if max_rate is not None:
            stmt = stmt.where(Guide.hourly_rate <= max_rate)
        if specialty:
            stmt = stmt.where(Guide.specialties.ilike(f"%{specialty}%"))

        if sort_by == "experience":
            stmt = stmt.order_by(Guide.guide_experience.desc().nulls_last())
        elif sort_by == "price_asc":
            stmt = stmt.order_by(Guide.hourly_rate.asc().nulls_last())
        elif sort_by == "price_desc":
            stmt = stmt.order_by(Guide.hourly_rate.desc().nulls_last())
        elif sort_by == "rating":
            stmt = stmt.order_by(Guide.avg_rating.desc().nulls_last())
        elif sort_by == "name":
            stmt = stmt.order_by(Guide.guide_name.asc())
        else:
            stmt = stmt.order_by(Guide.guide_experience.desc().nulls_last())

        stmt = stmt.offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def list_cities(self) -> list:
        """Return distinct cities where guides operate."""
        from sqlalchemy import func
        stmt = (
            select(Guide.guide_city, func.count(Guide.guide_id).label("count"))
            .where(Guide.guide_city.isnot(None))
            .group_by(Guide.guide_city)
            .order_by(func.count(Guide.guide_id).desc())
        )
        return [dict(row) for row in self.db.execute(stmt).mappings().all()]

    def list_languages(self) -> list:
        """Return distinct languages spoken by guides."""
        from sqlalchemy import func
        stmt = (
            select(Guide.guide_language, func.count(Guide.guide_id).label("count"))
            .where(Guide.guide_language.isnot(None))
            .group_by(Guide.guide_language)
            .order_by(func.count(Guide.guide_id).desc())
        )
        return [dict(row) for row in self.db.execute(stmt).mappings().all()]