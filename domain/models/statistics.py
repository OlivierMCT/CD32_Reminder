from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True)
class StatusStatistics:
    status: str
    count: int
    percentage: float


@dataclass(kw_only=True, frozen=True)
class CategoryStatistics:
    category_id: int
    title: str
    count: int
    percentage: float


@dataclass(kw_only=True, frozen=True)
class ReminderStatistics:
    total_todos: int
    by_status: list[StatusStatistics] = field(default_factory=list)
    by_category: list[CategoryStatistics] = field(default_factory=list)

