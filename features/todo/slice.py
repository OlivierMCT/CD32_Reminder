from datetime import datetime, timedelta
from typing import cast

from sqlalchemy.orm import Session

from domain.exceptions.reminder_error import ReminderError
from features.todo.schemas import TodoDto, TodoPostDto, TodoPutDto
from infrastructure.persistence.sqlalchemy.entities.category import CategoryEntity
from infrastructure.persistence.sqlalchemy.entities.todo import TodoEntity


def list_todos(session: Session) -> list[TodoEntity]:
    return cast(list[TodoEntity], session.query(TodoEntity).all())


def get_todo_by_id(session: Session, todo_id: int) -> TodoEntity | None:
    return cast(TodoEntity | None, session.get(TodoEntity, todo_id))


def create_todo(session: Session, dto: TodoPostDto) -> TodoEntity:
    validate_todo_post(dto)
    entity = TodoEntity(
        description=dto.desc.strip(),
        is_done=False,
        due_date=dto.due,
    )
    entity.creation_date = datetime.now()
    session.add(entity)
    session.flush()
    session.refresh(entity)
    return entity


def update_todo(session: Session, todo_id: int, dto: TodoPutDto) -> TodoEntity:
    validate_todo_put(dto)
    entity = get_todo_by_id(session, todo_id)
    if entity is None:
        raise ReminderError(666, f"Todo with id {todo_id} does not exist")

    entity.description = dto.desc.strip()
    entity.is_done = dto.done
    entity.due_date = dto.due
    entity.updated_date = datetime.now()
    session.add(entity)
    session.flush()
    session.refresh(entity)
    return entity


def toggle_todo(session: Session, todo_id: int) -> TodoEntity:
    entity = get_todo_by_id(session, todo_id)
    if entity is None:
        raise ReminderError(666, f"Todo with id {todo_id} does not exist")

    entity.is_done = not entity.is_done
    entity.updated_date = datetime.now()
    session.add(entity)
    session.flush()
    session.refresh(entity)
    return entity


def delete_todo(session: Session, todo_id: int) -> None:
    entity = get_todo_by_id(session, todo_id)
    if entity is None:
        raise ReminderError(666, f"Todo with id {todo_id} does not exist")
    if not is_todo_deletable(entity):
        raise ReminderError(999, f"Todo with id {todo_id} is not deletable")

    session.delete(entity)
    session.flush()


def add_categories_to_todo(session: Session, todo_id: int, *category_ids: int) -> TodoEntity:
    entity = get_todo_by_id(session, todo_id)
    if entity is None:
        raise ReminderError(666, f"Todo with id {todo_id} does not exist")

    existing_category_ids = {category.category_id for category in entity.categories}
    for category_id in [item for item in category_ids if item not in existing_category_ids]:
        category = session.get(CategoryEntity, category_id)
        if category is None:
            raise ReminderError(666, f"Category with id {category_id} does not exist")
        entity.categories.append(category)

    entity.updated_date = datetime.now()
    session.add(entity)
    session.flush()
    session.refresh(entity)
    return entity


def to_todo_dto(entity: TodoEntity) -> TodoDto:
    categories = list(entity.categories)
    return TodoDto(
        id=entity.todo_id,
        desc=entity.description,
        done=entity.is_done,
        due=entity.due_date,
        deletable=is_todo_deletable(entity),
        status=calculate_todo_status(entity),
        categories=[(category.category_id, category.title) for category in categories],
    )


def validate_todo_post(dto: TodoPostDto) -> None:
    description = dto.desc.strip()
    if not description or len(description) > 300:
        raise ReminderError(222, "Description must be between 1 and 300 characters")
    if dto.due is None or dto.due < datetime.today():
        raise ReminderError(222, "Due date must be present and greater than today's date")


def validate_todo_put(dto: TodoPutDto) -> None:
    description = dto.desc.strip()
    if not description or len(description) > 300:
        raise ReminderError(222, "Description must be between 1 and 300 characters")
    if dto.due is None:
        raise ReminderError(222, "Due date must be present")


def is_todo_deletable(entity: TodoEntity) -> bool:
    return entity.is_done and entity.due_date < datetime.today()


def calculate_todo_status(entity: TodoEntity) -> str:
    if entity.is_done:
        threshold = datetime.today() + timedelta(days=-7)
        return "archivé" if entity.due_date < threshold else "terminé"
    return "en cours" if entity.due_date >= datetime.today() else "en retard"


