from datetime import datetime

from sqlalchemy import Column, DateTime, Table, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class BaseEntity(DeclarativeBase):
    creation_date: Mapped[datetime] = mapped_column("created_at", DateTime, nullable=False)
    updated_date: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)


todos_categories = Table(
    "todos_categories",
    BaseEntity.metadata,
    Column("todo_id", Integer, ForeignKey("todos.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)