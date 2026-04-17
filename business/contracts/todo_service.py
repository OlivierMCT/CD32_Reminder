from abc import ABC, abstractmethod
from business.models.todo import Todo, TodoNew, TodoUpdate

class TodoService(ABC):
    @abstractmethod
    def find_all(self) -> list[Todo]: ...

    @abstractmethod
    def find_by_id(self, todo_id: int) -> Todo | None: ...

    @abstractmethod
    def search(self, keyword: str) -> list[Todo]: ...

    @abstractmethod
    def save_new(self, data: TodoNew) -> Todo: ...

    @abstractmethod
    def save_update(self, data: TodoUpdate) -> Todo: ...

    @abstractmethod
    def toggle(self, todo_id: int) -> Todo: ...

    @abstractmethod
    def remove(self, todo_id: int) -> Todo: ...

    @abstractmethod
    def add_categories(self, todo_id: int, *category_ids: int) -> Todo: ...

    @abstractmethod
    def remove_categories(self, todo_id: int, *category_ids: int) -> Todo: ...