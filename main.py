from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sample_data
from api.controllers.category_controller import router as category_router
from api.controllers.todo_controller import router as todo_router, get_todo_service
from business.contracts.category_service import CategoryService
from business.contracts.todo_service import TodoService
from business.services.category_service_impl import CategoryServiceImpl
from business.services.todo_service_impl import TodoServiceImpl
from persistence.entities.base_entity import BaseEntity
from persistence.entities.todo_entity import TodoEntity
from persistence.repositories.category_repository_impl import CategoryRepositoryImpl
from persistence.repositories.todo_repository_impl import TodoRepositoryImpl

app = FastAPI(title="CD32 Reminder", version="1.0")

app.include_router(todo_router)
app.include_router(category_router)

engine_db = create_engine('mysql://root:@localhost:3306/reminders')
BaseEntity.metadata.create_all(engine_db)

def _get_todo_service():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)()
    todo_repo = TodoRepositoryImpl(session)
    cat_repo = CategoryRepositoryImpl(session)
    try:
        yield TodoServiceImpl(todo_repo, cat_repo)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

def _get_category_service() -> CategoryService:
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)()
    cat_repo = CategoryRepositoryImpl(session)
    return CategoryServiceImpl(cat_repo)

#app.dependency_overrides[get_category_service] = _get_category_service
app.dependency_overrides[get_todo_service] = _get_todo_service



def seed():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)()
    if session.query(TodoEntity).count() == 0:
        sample_data.add_sample_data(session)
seed()