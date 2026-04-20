import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.persistence.sqlalchemy.base import BaseEntity
from infrastructure.persistence.sqlalchemy.entities.todo import TodoEntity
from infrastructure.persistence.sqlalchemy.seed import add_sample_data

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./reminders.db")
_engine_options = {}

if DATABASE_URL.startswith("sqlite"):
    # check_same_thread=False allows FastAPI request handlers to share the same DB file safely.
    _engine_options["connect_args"] = {"check_same_thread": False}

engine_db = create_engine(DATABASE_URL, **_engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine_db, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_schema() -> None:
    BaseEntity.metadata.create_all(engine_db)


def seed_database() -> None:
    session = SessionLocal()
    try:
        if session.query(TodoEntity).count() == 0:
            add_sample_data(session)
    finally:
        session.close()


def get_session() -> Session:
    return SessionLocal()

