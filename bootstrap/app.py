from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, cast

from bootstrap.database import create_schema, seed_database
from bootstrap.error_handlers import reminder_error_handler
from domain.exceptions.reminder_error import ReminderError
from features.category.router import router as category_router
from features.statistics.router import router as statistics_router
from features.todo.router import router as todo_router


def create_app() -> FastAPI:
    create_schema()
    seed_database()

    app = FastAPI(title="CD32 Reminder", version="1.0")

    app.include_router(todo_router)
    app.include_router(category_router)
    app.include_router(statistics_router)

    app.add_exception_handler(ReminderError, reminder_error_handler)

    app.add_middleware(
        cast(Any, CORSMiddleware),
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    return app


app = create_app()


