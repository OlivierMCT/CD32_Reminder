from fastapi import APIRouter, Depends
from fastapi.responses import Response

from api.dtos.todo import TodoDto
from business.contracts.todo_service import TodoService
from business.models.todo import Todo

router = APIRouter(prefix='/todo', tags=['todo'])

def get_todo_service() -> TodoService:
    raise NotImplementedError("This is a placeholder for the actual dependency injection of TodoService")

@router.get('/')
def get_all_todos(service: TodoService = Depends(get_todo_service)) -> list[TodoDto]:
    return [to_dto_from_model(m) for m in service.find_all()]

@router.get('/{id}', response_model=TodoDto)
def get_todo(id: int, service: TodoService = Depends(get_todo_service)):
    model = service.find_by_id(id)
    return to_dto_from_model(model) if model else Response(status_code=404, content='not found')

@router.delete('/{id}', status_code=204)
def delete_todo(id: int, service: TodoService = Depends(get_todo_service)):
    service.remove(id)

@router.patch('/{id}/category')
def update_todo_categories(id: int, body: dict, service: TodoService = Depends(get_todo_service)):
    service.add_categories(id, *body['categories'])
    # noinspection PyTypeChecker
    return to_dto_from_model(service.find_by_id(id))

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