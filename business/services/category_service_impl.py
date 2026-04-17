from business.contracts.category_service import CategoryService
from business.models.category import Category, CategoryUpdate, CategoryNew
from business.models.reminder_error import ReminderError
from persistence.contracts.category_repository import CategoryRepository
from persistence.entities.catagory_entity import CategoryEntity


class CategoryServiceImpl(CategoryService):
    def __init__(self, category_repo: CategoryRepository):
        self._category_repo = category_repo

    def to_category_from_entity(self, entity: CategoryEntity) -> Category:
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

    def find_all(self) -> list[Category]:
        return [self.to_category_from_entity(e) for e in self._category_repo.select_all()]

    def find_by_id(self, category_id: int) -> Category | None:
        entity = self._category_repo.select_by_id(category_id)
        return self.to_category_from_entity(entity) if entity else None

    def save_new(self, data: CategoryNew) -> Category:
        self.validate_category_new(data)
        entity = CategoryEntity(
            title=data.title.strip(),
            color=data.color.strip()
        )
        return self.to_category_from_entity(self._category_repo.insert(entity))

    def validate_category_new(self, data: CategoryNew) -> None:
        if not data.title.strip() or len(data.title.strip()) > 50:
            raise ReminderError(222, "Title must be between 1 and 50 characters")
        if not data.color.strip() or len(data.color.strip()) > 20:
            raise ReminderError(222, "Color must be between 1 and 20 characters")

    def save_update(self, data: CategoryUpdate) -> Category:
        self.validate_category_update(data)
        entity = self._category_repo.select_by_id(data.id)
        if entity is None:
            raise ReminderError(666, f"Category with id {data.id} does not exist")

        entity.title = data.title.strip()
        entity.color = data.color.strip()

        return self.to_category_from_entity(self._category_repo.update(entity))

    def validate_category_update(self, data: CategoryUpdate) -> None:
        if not data.title.strip() or len(data.title.strip()) > 50:
            raise ReminderError(222, "Title must be between 1 and 50 characters")
        if not data.color.strip() or len(data.color.strip()) > 20:
            raise ReminderError(222, "Color must be between 1 and 20 characters")

    def remove(self, category_id: int) -> Category:
        entity = self._category_repo.select_by_id(category_id)
        if entity is None:
            raise ReminderError(666, f"Category with id {category_id} does not exist")
        return self.to_category_from_entity(self._category_repo.delete(category_id))
