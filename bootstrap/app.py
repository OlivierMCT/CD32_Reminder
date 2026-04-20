from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bootstrap.database import create_schema, seed_database
from bootstrap.dependencies import build_category_service, build_statistics_service, build_todo_service
from bootstrap.error_handlers import reminder_error_handler
from domain.exceptions.reminder_error import ReminderError
from presentation.api.routers.category_router import router as category_router, get_category_service
from presentation.api.routers.statistics_router import router as statistics_router, get_statistics_service
from presentation.api.routers.todo_router import router as todo_router, get_todo_service


def create_app() -> FastAPI:
    create_schema()
    seed_database()

    app = FastAPI(title="CD32 Reminder", version="1.0")

    app.include_router(todo_router)
    app.include_router(category_router)
    app.include_router(statistics_router)

    app.add_exception_handler(ReminderError, reminder_error_handler)
    app.dependency_overrides[get_category_service] = build_category_service
    app.dependency_overrides[get_todo_service] = build_todo_service
    app.dependency_overrides[get_statistics_service] = build_statistics_service

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    return app


app = create_app()


