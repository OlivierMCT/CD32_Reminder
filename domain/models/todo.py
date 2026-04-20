from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from domain.models.category import Category

@dataclass(kw_only=True, frozen=True)
class Todo:
    id: int
    description: str
    is_done: bool
    status: TodoStatus
    due_date: datetime
    is_deletable: bool
    categories: list[Category] = field(default_factory=list)

class TodoStatus(str, Enum):
    LATE = "en retard"
    IN_PROGRESS = "en cours"
    CLOSED = "terminé"
    ARCHIVED = "archivé"

@dataclass(kw_only=True)
class TodoNew:
    description: str
    due_date: datetime

@dataclass(kw_only=True)
class TodoUpdate:
    id: int
    description: str
    is_done: bool
    due_date: datetime

