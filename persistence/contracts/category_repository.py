from abc import ABC, abstractmethod
from persistence.entities.category_entity import CategoryEntity


class CategoryRepository(ABC):
    @abstractmethod
    def select_all(self) -> list[type[CategoryEntity]]: ...

    @abstractmethod
    def select_by_id(self, todo_id: int) -> type[CategoryEntity] | None: ...

    @abstractmethod
    def insert(self, data: CategoryEntity) -> CategoryEntity: ...

    @abstractmethod
    def update(self, data: CategoryEntity) -> CategoryEntity: ...

    @abstractmethod
    def delete(self, category_id: int) -> type[CategoryEntity] | None: ...