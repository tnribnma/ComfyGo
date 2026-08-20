from typing import Any, Dict, Generic, List, Optional, Sequence, Type, TypeVar, Union
from typing_extensions import Self

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.exceptions import ConflictError, NotFoundError

ModelT = TypeVar("ModelT")


class GenericRepository(Generic[ModelT]):
    model: Type[ModelT]                  
    auto_commit: bool = True            

    def __init__(self, db: Session) -> None:
        self.db = db

    def _commit_or_flush(self) -> None:
        if self.auto_commit:
            self.db.commit()
        else:
            self.db.flush()

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        self.db.rollback()
        cause = str(exc.orig) if exc.orig else str(exc)
        raise ConflictError(
            "Resource already exists or violates a unique constraint",
            detail=cause,
        )

    def get(self, id: int) -> Optional[ModelT]:
        return self.db.get(self.model, id)

    def get_or_404(self, id: int) -> ModelT:
        obj = self.get(id)
        if obj is None:
            raise NotFoundError(
                f"{self.model.__name__} not found",
                detail=f"id={id}",
            )
        return obj

    def get_multi(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[ModelT]:
        stmt = select(self.model).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def get_by(self, **filters: Any) -> Sequence[ModelT]:
        stmt = select(self.model).filter_by(**filters)
        return self.db.scalars(stmt).all()

    def get_one_by(self, **filters: Any) -> Optional[ModelT]:
        stmt = select(self.model).filter_by(**filters)
        return self.db.scalars(stmt).first()

    def count(self, **filters: Any) -> int:
        stmt = select(func.count()).select_from(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        return int(self.db.scalar(stmt) or 0)

    def exists(self, id: int) -> bool:
        return self.get(id) is not None

    def create(self, data: Union[Dict[str, Any], ModelT]) -> ModelT:
        obj = self.model(**data) if isinstance(data, dict) else data
        self.db.add(obj)
        try:
            self._commit_or_flush()
        except IntegrityError as exc:
            self._handle_integrity_error(exc)
        if self.auto_commit:
            self.db.refresh(obj)
        return obj

    def create_many(self, items: List[Dict[str, Any]]) -> List[ModelT]:
        objs = [self.model(**i) for i in items]
        self.db.add_all(objs)
        try:
            self._commit_or_flush()
        except IntegrityError as exc:
            self._handle_integrity_error(exc)
        if self.auto_commit:
            for o in objs:
                self.db.refresh(o)
        return objs

    def update(self, id: int, data: Dict[str, Any]) -> ModelT:
        obj = self.get_or_404(id)
        for key, value in data.items():
            if hasattr(obj, key) and value is not None:
                setattr(obj, key, value)
        try:
            self._commit_or_flush()
        except IntegrityError as exc:
            self._handle_integrity_error(exc)
        if self.auto_commit:
            self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> None:
        """Hard delete by PK; raises NotFoundError if missing."""
        obj = self.get_or_404(id)
        self.db.delete(obj)
        try:
            self._commit_or_flush()
        except IntegrityError as exc:
            self._handle_integrity_error(exc)

    def delete_many(self, ids: List[int]) -> int:
        """Delete by PKs; returns number actually deleted."""
        if not ids:
            return 0
        stmt = select(self.model).where(
            getattr(self.model, self._pk_name()).in_(ids)
        )
        objs = self.db.scalars(stmt).all()
        for o in objs:
            self.db.delete(o)
        self._commit_or_flush()
        return len(objs)

    @classmethod
    def _pk_name(cls) -> str:
        """Return the model's primary key column name (best-effort)."""
        mapper = cls.model.__mapper__   
        return mapper.primary_key[0].name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} model={self.model.__name__}>"