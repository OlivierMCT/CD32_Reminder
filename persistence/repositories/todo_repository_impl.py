from datetime import datetime

from sqlalchemy.orm import Session

from persistence.contracts.todo_repository import TodoRepository
from persistence.entities.todo_entity import TodoEntity


class TodoRepositoryImpl(TodoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def select_all(self) -> list[type[TodoEntity]]:
        return self._session.query(TodoEntity).all()

    def select_by_id(self, todo_id: int) -> type[TodoEntity] | None:
        return self._session.get(TodoEntity, todo_id)

    def select_by_keyword(self, keyword: str) -> list[type[TodoEntity]]:
        return self._session.query(TodoEntity).filter(TodoEntity.description.ilike(f"%{keyword}%")).all()

    def insert(self, data: TodoEntity) -> TodoEntity:
        data.created_at = datetime.now()
        self._session.add(data)
        self._session.flush()
        self._session.refresh(data)
        return data

    def update(self, data: TodoEntity) -> TodoEntity:
        data.updated_date = datetime.now()
        self._session.add(data)
        self._session.flush()
        self._session.refresh(data)
        return data

    def delete(self, todo_id: int) -> type[TodoEntity] | None:
        entity = self.select_by_id(todo_id)
        if entity is None:
            return None
        self._session.delete(entity)
        self._session.flush()
        return entity

