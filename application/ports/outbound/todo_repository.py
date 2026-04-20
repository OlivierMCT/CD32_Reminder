from abc import ABC, abstractmethod

from application.ports.outbound.persistence_models import TodoData, TodoWriteModel

class TodoRepository(ABC):
    @abstractmethod
    def select_all(self) -> list[TodoData]: ...

    @abstractmethod
    def select_by_id(self, todo_id: int) -> TodoData | None: ...

    @abstractmethod
    def select_by_keyword(self, keyword: str) -> list[TodoData]: ...

    @abstractmethod
    def insert(self, data: TodoWriteModel) -> TodoData: ...

    @abstractmethod
    def update(self, data: TodoData) -> TodoData: ...

    @abstractmethod
    def delete(self, todo_id: int) -> TodoData | None: ...


