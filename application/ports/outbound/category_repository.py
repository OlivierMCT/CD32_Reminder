from abc import ABC, abstractmethod

from application.ports.outbound.persistence_models import CategoryData, CategoryWriteModel


class CategoryRepository(ABC):
    @abstractmethod
    def select_all(self) -> list[CategoryData]: ...

    @abstractmethod
    def select_by_id(self, category_id: int) -> CategoryData | None: ...

    @abstractmethod
    def insert(self, data: CategoryWriteModel) -> CategoryData: ...

    @abstractmethod
    def update(self, data: CategoryData) -> CategoryData: ...

    @abstractmethod
    def delete(self, category_id: int) -> CategoryData | None: ...


