from fastapi import APIRouter, Depends, Response

from application.ports.inbound.todo_service import TodoService
from domain.models.todo import Todo, TodoNew, TodoUpdate
from presentation.api.schemas.todo import TodoDto, TodoPostDto, TodoPutDto, TodoPatchDto

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

@router.post('/', status_code=201, response_model=TodoDto)
def post_todo(dto: TodoPostDto, response: Response, service: TodoService = Depends(get_todo_service)) -> TodoDto:
    model = service.save_new(to_model_from_postdto(dto))
    service.add_categories(model.id, *dto.categories)
    response.headers['Location'] = f'/todo/{model.id}'
    return to_dto_from_model(model)

@router.put('/{id}', response_model=TodoDto)
def put_todo(id: int, dto: TodoPutDto, service: TodoService = Depends(get_todo_service)) -> TodoDto:
    model = service.save_update(to_model_from_putdto(id, dto))
    return to_dto_from_model(model)

@router.patch('/{id}', response_model=TodoDto)
def patch_todo_status(id: int, dto: TodoPatchDto, service: TodoService = Depends(get_todo_service)):
    model = service.find_by_id(id)
    if model and model.is_done != dto.done:
        model = service.toggle(id)
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

def to_model_from_postdto(dto: TodoPostDto) -> TodoNew:
    return TodoNew(
        description=dto.desc,
        due_date=dto.due,
    )


def to_model_from_putdto(id: int, dto: TodoPutDto) -> TodoUpdate:
    return TodoUpdate(
        id=id,
        description=dto.desc,
        is_done=dto.done,
        due_date=dto.due,
    )
