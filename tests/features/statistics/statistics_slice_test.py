from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from features.statistics.slice import get_statistics
from infrastructure.persistence.sqlalchemy.base import BaseEntity
from infrastructure.persistence.sqlalchemy.entities.category import CategoryEntity
from infrastructure.persistence.sqlalchemy.entities.todo import TodoEntity


def build_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    BaseEntity.metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_local()


class TestStatisticsSlice:
    def test_should_compute_statistics_directly_from_database(self):
        session = build_session()
        now = datetime.today()
        try:
            perso = CategoryEntity(title="Perso", color="yellow")
            perso.creation_date = datetime.now()
            pro = CategoryEntity(title="Pro", color="blue")
            pro.creation_date = datetime.now()
            sport = CategoryEntity(title="Sport", color="green")
            sport.creation_date = datetime.now()
            session.add_all([perso, pro, sport])
            session.flush()

            todo_in_progress = TodoEntity(description="Todo 1", is_done=False, due_date=now + timedelta(days=2))
            todo_in_progress.creation_date = datetime.now()
            todo_in_progress.categories.append(perso)

            todo_late = TodoEntity(description="Todo 2", is_done=False, due_date=now - timedelta(days=1))
            todo_late.creation_date = datetime.now()
            todo_late.categories.append(pro)

            todo_closed = TodoEntity(description="Todo 3", is_done=True, due_date=now - timedelta(days=2))
            todo_closed.creation_date = datetime.now()
            todo_closed.categories.append(perso)

            todo_archived = TodoEntity(description="Todo 4", is_done=True, due_date=now - timedelta(days=10))
            todo_archived.creation_date = datetime.now()

            session.add_all([todo_in_progress, todo_late, todo_closed, todo_archived])
            session.commit()

            perso_id = perso.category_id
            pro_id = pro.category_id
            sport_id = sport.category_id

            stats = get_statistics(session)
        finally:
            session.close()

        assert stats.total_todos == 4

        status_map = {item.status: item for item in stats.by_status}
        assert status_map["en cours"].count == 1
        assert status_map["en retard"].count == 1
        assert status_map["terminé"].count == 1
        assert status_map["archivé"].count == 1
        assert status_map["en cours"].percentage == 25.0

        category_map = {item.category_id: item for item in stats.by_category}
        assert category_map[perso_id].count == 2
        assert category_map[perso_id].percentage == 50.0
        assert category_map[pro_id].count == 1
        assert category_map[pro_id].percentage == 25.0
        assert category_map[sport_id].count == 0
        assert category_map[sport_id].percentage == 0.0

    def test_should_return_zero_percentages_when_database_is_empty(self):
        session = build_session()
        try:
            stats = get_statistics(session)
        finally:
            session.close()

        assert stats.total_todos == 0
        assert all(item.percentage == 0.0 for item in stats.by_status)
        assert stats.by_category == []



