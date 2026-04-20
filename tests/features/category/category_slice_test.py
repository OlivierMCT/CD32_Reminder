import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.exceptions.reminder_error import ReminderError
from features.category.schemas import CategoryPostDto
from features.category.slice import create_category, to_category_dto, validate_category_post
from infrastructure.persistence.sqlalchemy.base import BaseEntity


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


class TestCategorySlice:
    def test_should_build_zero_progress_for_empty_category(self, session):
        entity = create_category(session, CategoryPostDto(title="Sport", color="blue"))

        dto = to_category_dto(entity)

        assert dto.todo_count == 0
        assert dto.todo_done == 0
        assert dto.progress_rate == 0.0

    def test_should_validate_title_and_color(self):
        with pytest.raises(ReminderError) as error:
            validate_category_post(CategoryPostDto(title="", color=" "))

        assert error.value.code == 222



