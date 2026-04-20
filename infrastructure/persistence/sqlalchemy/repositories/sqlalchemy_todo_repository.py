from datetime import datetime

from sqlalchemy.orm import Session

from application.ports.outbound.persistence_models import TodoData, TodoWriteModel
from application.ports.outbound.todo_repository import TodoRepository
from infrastructure.persistence.sqlalchemy.entities.todo import TodoEntity


class SqlAlchemyTodoRepository(TodoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def select_all(self) -> list[TodoData]:
        return self._session.query(TodoEntity).all()

    def select_by_id(self, todo_id: int) -> TodoData | None:
        return self._session.get(TodoEntity, todo_id)

    def select_by_keyword(self, keyword: str) -> list[TodoData]:
        return self._session.query(TodoEntity).filter(TodoEntity.description.ilike(f"%{keyword}%")).all()

    def insert(self, data: TodoWriteModel) -> TodoData:
        entity = TodoEntity(
            description=data.description,
            is_done=data.is_done,
            due_date=data.due_date,
        )
        entity.creation_date = datetime.now()
        self._session.add(entity)
        self._session.flush()
        self._session.refresh(entity)
        return entity

    def update(self, data: TodoData) -> TodoData:
        data.updated_date = datetime.now()
        self._session.add(data)
        self._session.flush()
        self._session.refresh(data)
        return data

    def delete(self, todo_id: int) -> TodoData | None:
        entity = self.select_by_id(todo_id)
        if entity is None:
            return None
        self._session.delete(entity)
        self._session.flush()
        return entity




