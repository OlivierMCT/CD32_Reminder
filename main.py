from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.controllers.category_controller import router as category_router
from api.controllers.todo_controller import router as todo_router
from business.contracts.category_service import CategoryService
from business.contracts.todo_service import TodoService
from business.services.category_service_impl import CategoryServiceImpl
from business.services.todo_service_impl import TodoServiceImpl
from persistence.entities.base_entity import BaseEntity
from persistence.repositories.category_repository_impl import CategoryRepositoryImpl
from persistence.repositories.todo_repository_impl import TodoRepositoryImpl

app = FastAPI(title="CD32 Reminder", version="1.0")

app.include_router(todo_router)
app.include_router(category_router)

engine_db = create_engine('mysql://root:@localhost:3306/reminders')
BaseEntity.metadata.create_all(engine_db)

def get_todo_service() -> TodoService:
    session = sessionmaker(autocommit=False, autoflush=False, engine_db=engine_db)()
    todo_repo = TodoRepositoryImpl(session)
    cat_repo = CategoryRepositoryImpl(session)
    return TodoServiceImpl(todo_repo, cat_repo)

def get_category_service() -> CategoryService:
    session = sessionmaker(autocommit=False, autoflush=False, engine_db=engine_db)()
    cat_repo = CategoryRepositoryImpl(session)
    return CategoryServiceImpl(cat_repo)

app.dependency_overrides[get_category_service] = get_category_service
app.dependency_overrides[get_todo_service] = get_todo_service
