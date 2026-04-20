from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from features.statistics.schemas import CategoryStatisticsDto, ReminderStatisticsDto, StatusStatisticsDto
from infrastructure.persistence.sqlalchemy.base import todos_categories
from infrastructure.persistence.sqlalchemy.entities.category import CategoryEntity
from infrastructure.persistence.sqlalchemy.entities.todo import TodoEntity


def get_statistics(session: Session) -> ReminderStatisticsDto:
    todo_rows = session.query(TodoEntity.is_done, TodoEntity.due_date).all()
    total_todos = len(todo_rows)

    status_counts = {
        "en retard": 0,
        "en cours": 0,
        "terminé": 0,
        "archivé": 0,
    }

    for is_done, due_date in todo_rows:
        status_counts[resolve_status(is_done=is_done, due_date=due_date)] += 1

    category_rows = (
        session.query(
            CategoryEntity.category_id,
            CategoryEntity.title,
            func.count(todos_categories.c.todo_id).label("todo_count"),
        )
        .outerjoin(todos_categories, CategoryEntity.category_id == todos_categories.c.category_id)
        .group_by(CategoryEntity.category_id, CategoryEntity.title)
        .order_by(CategoryEntity.category_id)
        .all()
    )

    return ReminderStatisticsDto(
        total_todos=total_todos,
        by_status=[
            StatusStatisticsDto(
                status=status,
                count=count,
                percentage=to_percentage(count, total_todos),
            )
            for status, count in status_counts.items()
        ],
        by_category=[
            CategoryStatisticsDto(
                category_id=category_id,
                title=title,
                count=todo_count,
                percentage=to_percentage(todo_count, total_todos),
            )
            for category_id, title, todo_count in category_rows
        ],
    )


def resolve_status(*, is_done: bool, due_date: datetime) -> str:
    if is_done:
        archive_threshold = datetime.today() + timedelta(days=-7)
        return "archivé" if due_date < archive_threshold else "terminé"
    return "en cours" if due_date >= datetime.today() else "en retard"


def to_percentage(count: int, total: int) -> float:
    return round((count / total) * 100, 2) if total else 0.0

