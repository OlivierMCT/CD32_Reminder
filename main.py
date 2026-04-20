import os

from fastapi import FastAPI, Request
from fastapi.middleware import cors
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

import sample_data
from api.controllers.category_controller import router as category_router, get_category_service
from api.controllers.todo_controller import router as todo_router, get_todo_service
from business.contracts.category_service import CategoryService
from business.models.reminder_error import ReminderError
from business.services.category_service_impl import CategoryServiceImpl
from business.services.todo_service_impl import TodoServiceImpl
from persistence.entities.base_entity import BaseEntity
from persistence.entities.todo_entity import TodoEntity
from persistence.repositories.category_repository_impl import CategoryRepositoryImpl
from persistence.repositories.todo_repository_impl import TodoRepositoryImpl

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./reminders.db")
engine_options = {}

if DATABASE_URL.startswith("sqlite"):
    # check_same_thread=False allows FastAPI request handlers to share the same DB file safely.
    engine_options["connect_args"] = {"check_same_thread": False}

engine_db = create_engine(DATABASE_URL, **engine_options)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine_db, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

BaseEntity.metadata.create_all(engine_db)

def seed():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)()
    if session.query(TodoEntity).count() == 0:
        sample_data.add_sample_data(session)
seed()

async def reminder_error_handler(request: Request, error: ReminderError) -> JSONResponse:
    status_code = 400
    if error.code == 666: status_code = 404
    elif error.code == 999: status_code = 403
    elif error.code == 222: status_code = 400
    return JSONResponse(status_code=status_code, content=error.message)

def _get_todo_service():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)()
    todo_repo = TodoRepositoryImpl(session)
    cat_repo = CategoryRepositoryImpl(session)
    return TodoServiceImpl(todo_repo, cat_repo)

def _get_category_service() -> CategoryService:
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine_db)()
    cat_repo = CategoryRepositoryImpl(session)
    return CategoryServiceImpl(cat_repo)

app = FastAPI(title="CD32 Reminder", version="1.0")

app.include_router(todo_router)
app.include_router(category_router)

app.add_exception_handler(ReminderError, reminder_error_handler)
app.dependency_overrides[get_category_service] = _get_category_service
app.dependency_overrides[get_todo_service] = _get_todo_service

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=True,
)

