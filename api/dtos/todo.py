from datetime import datetime

from pydantic.dataclasses import dataclass

@dataclass
class TodoDto:
    id: int
    desc: str
    done: bool
    status: str
    due: datetime
    deletable: bool
    categories: list[tuple[int, str]]