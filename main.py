from fastapi import FastAPI

from api.controllers.category_controller import router as category_router
from api.controllers.todo_controller import router as todo_router

app = FastAPI(title="CD32 Reminder", version="1.0")

app.include_router(todo_router)
app.include_router(category_router)
