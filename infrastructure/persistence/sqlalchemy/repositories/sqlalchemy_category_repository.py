from datetime import datetime

from sqlalchemy.orm import Session

from application.ports.outbound.persistence_models import CategoryData, CategoryWriteModel
from application.ports.outbound.category_repository import CategoryRepository
from infrastructure.persistence.sqlalchemy.entities.category import CategoryEntity


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def select_all(self) -> list[CategoryData]:
        return self._session.query(CategoryEntity).all()

    def select_by_id(self, category_id: int) -> CategoryData | None:
        return self._session.get(CategoryEntity, category_id)

    def insert(self, data: CategoryWriteModel) -> CategoryData:
        entity = CategoryEntity(
            title=data.title,
            color=data.color,
        )
        entity.creation_date = datetime.now()
        self._session.add(entity)
        self._session.flush()
        self._session.refresh(entity)
        return entity

    def update(self, data: CategoryData) -> CategoryData:
        data.updated_date = datetime.now()
        self._session.add(data)
        self._session.flush()
        self._session.refresh(data)
        return data

    def delete(self, category_id: int) -> CategoryData | None:
        entity = self.select_by_id(category_id)
        if not entity:
            return None
        self._session.delete(entity)
        self._session.flush()
        return entity





