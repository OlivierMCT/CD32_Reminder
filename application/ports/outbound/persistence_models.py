from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Protocol


@dataclass(kw_only=True)
class TodoWriteModel:
    description: str
    is_done: bool
    due_date: datetime


@dataclass(kw_only=True)
class CategoryWriteModel:
    title: str
    color: str


class TodoData(Protocol):
    todo_id: int
    description: str
    is_done: bool
    due_date: datetime
    creation_date: datetime
    updated_date: datetime | None
    categories: Iterable[CategoryData]


class CategoryData(Protocol):
    category_id: int
    title: str
    color: str
    creation_date: datetime
    updated_date: datetime | None
    todos: Iterable[TodoData]


