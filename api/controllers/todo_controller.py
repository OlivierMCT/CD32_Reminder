from fastapi import APIRouter

from api.dtos.todo import TodoDto
from business.contracts.todo_service import TodoService
from business.models.todo import Todo

router = APIRouter(prefix='/todo', tags=['todo'])

@router.get('/')
def get_all_todos(service: TodoService) -> list[TodoDto]:
    return [to_dto_from_model(m) for m in service.find_all()]

def to_dto_from_model(model: Todo) -> TodoDto:
    return TodoDto(
        id=model.id,
        desc=model.description,
        done=model.is_done,
        due=model.due_date,
        deletable=model.is_deletable,
        status=model.status,
        categories=[(c.id, c.title) for c in model.categories]
    )