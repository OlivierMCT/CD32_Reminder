from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.exceptions.reminder_error import ReminderError
from features.todo.schemas import TodoPostDto
from features.todo.slice import add_categories_to_todo, create_todo, delete_todo, to_todo_dto
from infrastructure.persistence.sqlalchemy.base import BaseEntity
from infrastructure.persistence.sqlalchemy.entities.category import CategoryEntity


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    BaseEntity.metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = session_local()
    try:
        yield db_session
    finally:
        db_session.close()


class TestTodoSlice:
    def test_should_create_todo_and_attach_categories(self, session):
        category = CategoryEntity(title="Perso", color="yellow")
        category.creation_date = datetime.now()
        session.add(category)
        session.commit()
        session.refresh(category)

        todo = create_todo(
            session,
            TodoPostDto(
                desc="Apprendre vertical slices",
                due=datetime.today() + timedelta(days=2),
                categories=[category.category_id],
            ),
        )
        todo = add_categories_to_todo(session, todo.todo_id, category.category_id)

        dto = to_todo_dto(todo)

        assert dto.desc == "Apprendre vertical slices"
        assert dto.status == "en cours"
        assert dto.categories == [(category.category_id, "Perso")]

    def test_should_refuse_to_delete_non_deletable_todo(self, session):
        todo = create_todo(
            session,
            TodoPostDto(
                desc="Todo non supprimable",
                due=datetime.today() + timedelta(days=2),
                categories=[],
            ),
        )

        with pytest.raises(ReminderError) as error:
            delete_todo(session, todo.todo_id)

        assert error.value.code == 999


