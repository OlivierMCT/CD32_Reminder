from pydantic.dataclasses import dataclass


@dataclass
class CategoryDto:
    id: int
    title: str
    color: str
    todo_count: int
    todo_done: int
    progress_rate: float


@dataclass
class CategoryPostDto:
    title: str
    color: str


@dataclass
class CategoryPutDto:
    title: str
    color: str

