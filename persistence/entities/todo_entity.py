from datetime import datetime
from sqlalchemy.orm import relationship
from persistence.entities.base_entity import BaseEntity
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class TodoEntity(BaseEntity):
    __tablename__ = 'todos'

    todo_id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    description: str = Column("description", String(500), nullable=False)
    is_done: bool = Column("done", Boolean, default=False)
    due_date: datetime = Column("due_date", DateTime, nullable=False)
    categories = relationship("CategoryEntity", secondary="todos_categories", back_populates="todos", lazy="dynamic")
