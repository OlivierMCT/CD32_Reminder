from pydantic.dataclasses import dataclass


@dataclass
class StatusStatisticsDto:
    status: str
    count: int
    percentage: float


@dataclass
class CategoryStatisticsDto:
    category_id: int
    title: str
    count: int
    percentage: float


@dataclass
class ReminderStatisticsDto:
    total_todos: int
    by_status: list[StatusStatisticsDto]
    by_category: list[CategoryStatisticsDto]

