from functools import lru_cache
from typing import Any, Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from models.base_entity import BaseEntity


def create_db_and_tables(engine: Engine):
    BaseEntity.metadata.create_all(engine)


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    sqlite_file_name = "user-service.db"
    sqlite_url = f"sqlite:////app/data/{sqlite_file_name}"

    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False}
    )

    return engine


def get_session() -> Generator[Session, Any, None]:
    engine = get_engine()
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# TODO: Implement @transaction annotation
