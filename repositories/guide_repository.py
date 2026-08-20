from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Guide
from .base import GenericRepository


class GuideRepository(GenericRepository[Guide]):
    model = Guide

    def get_by_email(self, email: str):
        stmt = select(Guide).where(Guide.guide_email == email)
        return self.db.scalars(stmt).first()

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