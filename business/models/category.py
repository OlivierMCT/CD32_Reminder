from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class Category:
    id: int
    title: str
    color: str
    todo_count: int
    todo_done: int
    progress_rate: float

@dataclass(kw_only=True)
class CategoryNew:
    title: str
    color: str

@dataclass(kw_only=True)
class CategoryUpdate:
    id: int
    title: str
    color: str