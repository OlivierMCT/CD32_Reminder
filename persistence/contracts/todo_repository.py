from abc import ABC, abstractmethod
from persistence.entities.todo_entity import TodoEntity

class TodoRepository(ABC):
    @abstractmethod
    def select_all(self) -> list[TodoEntity]: ...

    @abstractmethod
    def select_by_id(self, todo_id: int) -> TodoEntity | None: ...

    @abstractmethod
    def select_by_keyword(self, keyword: str) -> list[TodoEntity]: ...

    @abstractmethod
    def insert(self, data: TodoEntity) -> TodoEntity: ...

    @abstractmethod
    def update(self, data: TodoEntity) -> TodoEntity: ...

    @abstractmethod
    def delete(self, todo_id: int) -> TodoEntity: ...
