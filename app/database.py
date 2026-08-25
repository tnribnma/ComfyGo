import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .config import settings
from .models.base import Base  

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

__all__ = ["Base", "Database", "get_db", "db_scope"]


class Database:
    _engine = None
    _session_factory = None

    @classmethod
    def engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                settings.database_url,
                pool_pre_ping=True,   
                pool_size=10,
                max_overflow=20,
                pool_recycle=1800,    
                echo=False,
                future=True,
            )
        return cls._engine

    @classmethod
    def session_factory(cls):
        if cls._session_factory is None:
            cls._session_factory = sessionmaker(
                bind=cls.engine(),
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,  
            )
        return cls._session_factory

    @classmethod
    def create_all(cls) -> None:
        Base.metadata.create_all(cls.engine())

    @classmethod
    def drop_all(cls) -> None:
        Base.metadata.drop_all(cls.engine())

    @classmethod
    def dispose(cls) -> None:
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None


def get_db() -> Generator[Session, None, None]:
  
    session: Session = Database.session_factory()()
    try:
        yield session
    finally:
        session.close()

@contextmanager
def db_scope() -> Generator[Session, None, None]:
 
    session: Session = Database.session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()