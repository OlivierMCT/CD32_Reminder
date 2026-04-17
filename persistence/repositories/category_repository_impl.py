from datetime import datetime

from sqlalchemy.orm import Session

from persistence.contracts.category_repository import CategoryRepository
from persistence.entities.category_entity import CategoryEntity


class CategoryRepositoryImpl(CategoryRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def select_all(self) -> list[type[CategoryEntity]]:
        return self._session.query(CategoryEntity).all()

    def select_by_id(self, todo_id: int) -> type[CategoryEntity] | None:
        return self._session.query(CategoryEntity).get(todo_id)

    def insert(self, data: CategoryEntity) -> CategoryEntity:
        data.creation_date = datetime.now()
        self._session.add(data)
        self._session.flush()
        self._session.refresh(data)
        return data

    def update(self, data: CategoryEntity) -> CategoryEntity:
        data.updated_date = datetime.now()
        self._session.add(data)
        self._session.flush()
        self._session.refresh(data)
        return data

    def delete(self, category_id: int) -> type[CategoryEntity] | None:
        entity = self.select_by_id(category_id)
        if not entity:
            return None
        self._session.delete(entity)
        self._session.flush()
        return entity

