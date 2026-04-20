from application.ports.inbound.category_service import CategoryService
from application.ports.inbound.statistics_service import StatisticsService
from application.ports.inbound.todo_service import TodoService
from application.use_cases.category_service import CategoryServiceImpl
from application.use_cases.statistics_service import StatisticsServiceImpl
from application.use_cases.todo_service import TodoServiceImpl
from bootstrap.database import get_session
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_todo_repository import SqlAlchemyTodoRepository


def build_todo_service() -> TodoService:
    session = get_session()
    todo_repository = SqlAlchemyTodoRepository(session)
    category_repository = SqlAlchemyCategoryRepository(session)
    return TodoServiceImpl(todo_repository, category_repository)


def build_category_service() -> CategoryService:
    session = get_session()
    category_repository = SqlAlchemyCategoryRepository(session)
    return CategoryServiceImpl(category_repository)


def build_statistics_service() -> StatisticsService:
    session = get_session()
    todo_repository = SqlAlchemyTodoRepository(session)
    category_repository = SqlAlchemyCategoryRepository(session)
    return StatisticsServiceImpl(todo_repository, category_repository)


