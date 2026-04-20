from datetime import datetime
from typing import cast

from sqlalchemy.orm import Session

from domain.exceptions.reminder_error import ReminderError
from features.category.schemas import CategoryDto, CategoryPostDto, CategoryPutDto
from infrastructure.persistence.sqlalchemy.entities.category import CategoryEntity


def list_categories(session: Session) -> list[CategoryEntity]:
    return cast(list[CategoryEntity], session.query(CategoryEntity).all())


def get_category_by_id(session: Session, category_id: int) -> CategoryEntity | None:
    return cast(CategoryEntity | None, session.get(CategoryEntity, category_id))


def create_category(session: Session, dto: CategoryPostDto) -> CategoryEntity:
    validate_category_post(dto)
    entity = CategoryEntity(
        title=dto.title.strip(),
        color=dto.color.strip(),
    )
    entity.creation_date = datetime.now()
    session.add(entity)
    session.flush()
    session.refresh(entity)
    return entity


def update_category(session: Session, category_id: int, dto: CategoryPutDto) -> CategoryEntity:
    validate_category_put(dto)
    entity = get_category_by_id(session, category_id)
    if entity is None:
        raise ReminderError(666, f"Category with id {category_id} does not exist")

    entity.title = dto.title.strip()
    entity.color = dto.color.strip()
    entity.updated_date = datetime.now()
    session.add(entity)
    session.flush()
    session.refresh(entity)
    return entity


def delete_category(session: Session, category_id: int) -> None:
    entity = get_category_by_id(session, category_id)
    if entity is None:
        raise ReminderError(666, f"Category with id {category_id} does not exist")

    session.delete(entity)
    session.flush()


def to_category_dto(entity: CategoryEntity) -> CategoryDto:
    todo_count = len(entity.todos)
    todo_done = len([todo for todo in entity.todos if todo.is_done])
    progress_rate = (todo_done / todo_count) if todo_count else 0.0
    return CategoryDto(
        id=entity.category_id,
        title=entity.title,
        color=entity.color,
        todo_count=todo_count,
        todo_done=todo_done,
        progress_rate=progress_rate,
    )


def validate_category_post(dto: CategoryPostDto) -> None:
    title = dto.title.strip()
    color = dto.color.strip()
    if not title or len(title) > 50:
        raise ReminderError(222, "Title must be between 1 and 50 characters")
    if not color or len(color) > 20:
        raise ReminderError(222, "Color must be between 1 and 20 characters")


def validate_category_put(dto: CategoryPutDto) -> None:
    validate_category_post(CategoryPostDto(title=dto.title, color=dto.color))


