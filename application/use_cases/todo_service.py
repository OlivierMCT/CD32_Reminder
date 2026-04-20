from datetime import datetime, timedelta

from application.ports.inbound.todo_service import TodoService
from application.ports.outbound.category_repository import CategoryRepository
from application.ports.outbound.persistence_models import CategoryData, TodoData, TodoWriteModel
from application.ports.outbound.todo_repository import TodoRepository
from domain.exceptions.reminder_error import ReminderError
from domain.models.category import Category
from domain.models.todo import Todo, TodoUpdate, TodoNew, TodoStatus


class TodoServiceImpl(TodoService):
    def __init__(self, todo_repo: TodoRepository, category_repo: CategoryRepository):
        self._todo_repo = todo_repo
        self._category_repo = category_repo

    def find_all(self) -> list[Todo]:
        return [self.to_todo_from_entity(e) for e in self._todo_repo.select_all()]

    def find_by_id(self, todo_id: int) -> Todo | None:
        entity = self._todo_repo.select_by_id(todo_id)
        return self.to_todo_from_entity(entity) if entity else None

    def search(self, keyword: str) -> list[Todo]:
        return [self.to_todo_from_entity(e) for e in self._todo_repo.select_by_keyword(keyword)]

    def save_new(self, data: TodoNew) -> Todo:
        self.validate_todo_new(data)
        entity = TodoWriteModel(
            description=data.description.strip(),
            is_done=False,
            due_date=data.due_date
        )
        entity = self._todo_repo.insert(entity)
        return self.to_todo_from_entity(entity)

    def validate_todo_new(self, data: TodoNew) -> None:
        if not data.description.strip() or len(data.description.strip()) > 300:
            raise ReminderError(222, "Description must be between 1 and 300 characters")
        if data.due_date is None or data.due_date < datetime.today():
            raise ReminderError(222, "Due date must be present and greater than today's date")

    def save_update(self, data: TodoUpdate) -> Todo:
        self.validate_todo_update(data)
        entity = self._todo_repo.select_by_id(data.id)
        if entity is None:
            raise ReminderError(666, f"Todo with id {data.id} does not exist")

        entity.description = data.description.strip()
        entity.due_date = data.due_date
        entity.is_done = data.is_done

        entity = self._todo_repo.update(entity)
        return self.to_todo_from_entity(entity)

    def validate_todo_update(self, data: TodoUpdate) -> None:
        if not data.description.strip() or len(data.description.strip()) > 300:
            raise ReminderError(222, "Description must be between 1 and 300 characters")
        if data.due_date is None:
            raise ReminderError(222, "Due date must be present")

    def toggle(self, todo_id: int) -> Todo:
        entity = self._todo_repo.select_by_id(todo_id)
        if entity is None:
            raise ReminderError(666, f"Todo with id {todo_id} does not exist")

        entity.is_done = not entity.is_done

        entity = self._todo_repo.update(entity)
        return self.to_todo_from_entity(entity)

    def remove(self, todo_id: int) -> Todo:
        entity = self._todo_repo.select_by_id(todo_id)
        if entity is None:
            raise ReminderError(666, f"Todo with id {todo_id} does not exist")
        model = self.to_todo_from_entity(entity)
        if not model.is_deletable:
            raise ReminderError(999, f'Todo with id {todo_id} is not deletable')
        self._todo_repo.delete(todo_id)
        return model

    def to_todo_from_entity(self, entity: TodoData) -> Todo:
        return Todo(
            id=entity.todo_id,
            description=entity.description,
            is_done=entity.is_done,
            due_date=entity.due_date,
            is_deletable=self.calculate_is_deletable(entity),
            status=self.calculate_status(entity),
            categories=[self.to_category_from_entity(c) for c in entity.categories]
        )

    def calculate_is_deletable(self, entity: TodoData) -> bool:
        return entity.is_done and entity.due_date < datetime.today()

    def calculate_status(self, entity: TodoData) -> TodoStatus:
        if entity.is_done:
            return TodoStatus.ARCHIVED if entity.due_date < datetime.today() + timedelta(days=-7) else TodoStatus.CLOSED
        else:
            return TodoStatus.IN_PROGRESS if entity.due_date >= datetime.today() else TodoStatus.LATE

    def to_category_from_entity(self, entity: CategoryData) -> Category:
        todo_count = len(entity.todos)
        todo_done = len([e for e in entity.todos if e.is_done])
        return Category(
            id=entity.category_id,
            color=entity.color,
            title=entity.title,
            todo_count=todo_count,
            todo_done=todo_done,
            progress_rate=todo_done / todo_count,
        )

    def add_categories(self, todo_id: int, *category_ids: int) -> Todo:
        entity = self._todo_repo.select_by_id(todo_id)
        if entity is None:
            raise ReminderError(666, f"Todo with id {todo_id} does not exist")

        entity_categories = [c.category_id for c in entity.categories]
        for category_id in [id for id in category_ids if not id in entity_categories]:
            e = self._category_repo.select_by_id(category_id)
            if e is None:
                raise ReminderError(666, f"Category with id {category_id} does not exist")
            entity.categories.append(e)
        entity = self._todo_repo.update(entity)
        return self.to_todo_from_entity(entity)

    def remove_categories(self, todo_id: int, *category_ids: int) -> Todo:
        entity = self._todo_repo.select_by_id(todo_id)
        if entity is None:
            raise ReminderError(666, f"Todo with id {todo_id} does not exist")
        for category_id in category_ids:
            e = self._category_repo.select_by_id(category_id)
            if e is not None:
                entity.categories.remove(e)
        entity = self._todo_repo.update(entity)
        return self.to_todo_from_entity(entity)


