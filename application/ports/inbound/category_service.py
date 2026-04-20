from abc import ABC, abstractmethod

from domain.models.category import Category, CategoryNew, CategoryUpdate

class CategoryService(ABC):
    @abstractmethod
    def find_all(self) -> list[Category]: ...

    @abstractmethod
    def find_by_id(self, category_id: int) -> Category | None: ...

    @abstractmethod
    def save_new(self, data: CategoryNew) -> Category: ...

    @abstractmethod
    def save_update(self, data: CategoryUpdate) -> Category: ...

    @abstractmethod
    def remove(self, category_id: int) -> Category: ...
