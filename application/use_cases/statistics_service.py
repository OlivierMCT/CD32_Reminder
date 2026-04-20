from datetime import datetime, timedelta

from application.ports.inbound.statistics_service import StatisticsService
from application.ports.outbound.category_repository import CategoryRepository
from application.ports.outbound.persistence_models import TodoData
from application.ports.outbound.todo_repository import TodoRepository
from domain.models.statistics import CategoryStatistics, ReminderStatistics, StatusStatistics
from domain.models.todo import TodoStatus


class StatisticsServiceImpl(StatisticsService):
    def __init__(self, todo_repo: TodoRepository, category_repo: CategoryRepository):
        self._todo_repo = todo_repo
        self._category_repo = category_repo

    def get_statistics(self) -> ReminderStatistics:
        todos = self._todo_repo.select_all()
        categories = self._category_repo.select_all()

        total_todos = len(todos)

        status_count = {
            TodoStatus.LATE.value: 0,
            TodoStatus.IN_PROGRESS.value: 0,
            TodoStatus.CLOSED.value: 0,
            TodoStatus.ARCHIVED.value: 0,
        }

        for todo in todos:
            resolved_status = self._calculate_status(todo)
            status_count[resolved_status.value] += 1

        by_status = [
            StatusStatistics(
                status=status,
                count=count,
                percentage=self._to_percentage(count, total_todos),
            )
            for status, count in status_count.items()
        ]

        by_category = []
        for category in categories:
            category_todos_count = len(list(category.todos))
            by_category.append(
                CategoryStatistics(
                    category_id=category.category_id,
                    title=category.title,
                    count=category_todos_count,
                    percentage=self._to_percentage(category_todos_count, total_todos),
                )
            )

        return ReminderStatistics(
            total_todos=total_todos,
            by_status=by_status,
            by_category=by_category,
        )

    def _calculate_status(self, entity: TodoData) -> TodoStatus:
        if entity.is_done:
            return TodoStatus.ARCHIVED if entity.due_date < datetime.today() + timedelta(days=-7) else TodoStatus.CLOSED
        return TodoStatus.IN_PROGRESS if entity.due_date >= datetime.today() else TodoStatus.LATE

    def _to_percentage(self, count: int, total: int) -> float:
        return round((count / total) * 100, 2) if total else 0.0


