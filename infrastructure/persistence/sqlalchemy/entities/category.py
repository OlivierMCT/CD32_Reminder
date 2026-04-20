from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.persistence.sqlalchemy.base import BaseEntity

class CategoryEntity(BaseEntity):
    __tablename__ = 'categories'

    category_id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    title: str = Column("title", String(50), nullable=False, unique=True)
    color: str = Column("color", String(20), nullable=False)
    todos = relationship("TodoEntity", secondary="todos_categories", back_populates="categories", lazy="selectin")
