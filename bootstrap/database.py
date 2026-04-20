from infrastructure.db import SessionLocal, engine
from infrastructure.persistence.sqlalchemy.base import BaseEntity
from infrastructure.persistence.sqlalchemy.entities.todo import TodoEntity
from infrastructure.persistence.sqlalchemy.seed import add_sample_data


def create_schema() -> None:
    BaseEntity.metadata.create_all(engine)


def seed_database() -> None:
    session = SessionLocal()
    try:
        if session.query(TodoEntity).count() == 0:
            add_sample_data(session)
    finally:
        session.close()


