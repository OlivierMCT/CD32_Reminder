from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import MagicMock

from application.ports.outbound.category_repository import CategoryRepository
from application.ports.outbound.todo_repository import TodoRepository
from application.use_cases.statistics_service import StatisticsServiceImpl
from domain.models.todo import TodoStatus


class TestStatisticsService:
    def test_should_compute_statistics_by_status_and_category(self):
        # Arrange
        now = datetime.today()
        todos = [
            SimpleNamespace(is_done=False, due_date=now + timedelta(days=2)),
            SimpleNamespace(is_done=False, due_date=now - timedelta(days=1)),
            SimpleNamespace(is_done=True, due_date=now - timedelta(days=2)),
            SimpleNamespace(is_done=True, due_date=now - timedelta(days=10)),
        ]
        categories = [
            SimpleNamespace(category_id=1, title="Perso", todos=[todos[0], todos[2]]),
            SimpleNamespace(category_id=2, title="Pro", todos=[todos[1]]),
            SimpleNamespace(category_id=3, title="Sport", todos=[]),
        ]

        todo_repo = MagicMock(spec=TodoRepository)
        todo_repo.select_all.return_value = todos
        category_repo = MagicMock(spec=CategoryRepository)
        category_repo.select_all.return_value = categories

        service = StatisticsServiceImpl(todo_repo, category_repo)

        # Act
        stats = service.get_statistics()

        # Assert
        assert stats.total_todos == 4

        status_map = {item.status: item for item in stats.by_status}
        assert status_map[TodoStatus.IN_PROGRESS.value].count == 1
        assert status_map[TodoStatus.LATE.value].count == 1
        assert status_map[TodoStatus.CLOSED.value].count == 1
        assert status_map[TodoStatus.ARCHIVED.value].count == 1
        assert status_map[TodoStatus.IN_PROGRESS.value].percentage == 25.0

        category_map = {item.category_id: item for item in stats.by_category}
        assert category_map[1].count == 2
        assert category_map[1].percentage == 50.0
        assert category_map[2].count == 1
        assert category_map[2].percentage == 25.0
        assert category_map[3].count == 0
        assert category_map[3].percentage == 0.0

    def test_should_return_zero_percentages_when_no_todo(self):
        # Arrange
        todo_repo = MagicMock(spec=TodoRepository)
        todo_repo.select_all.return_value = []
        category_repo = MagicMock(spec=CategoryRepository)
        category_repo.select_all.return_value = [
            SimpleNamespace(category_id=1, title="Perso", todos=[]),
        ]

        service = StatisticsServiceImpl(todo_repo, category_repo)

        # Act
        stats = service.get_statistics()

        # Assert
        assert stats.total_todos == 0
        assert all(item.percentage == 0.0 for item in stats.by_status)
        assert stats.by_category[0].percentage == 0.0

