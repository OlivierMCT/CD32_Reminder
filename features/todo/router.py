from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from features.shared.db import get_db_session
from features.todo.schemas import TodoDto, TodoPatchDto, TodoPostDto, TodoPutDto
from features.todo.slice import (
    add_categories_to_todo,
    create_todo,
    delete_todo,
    get_todo_by_id,
    list_todos,
    to_todo_dto,
    toggle_todo,
    update_todo,
)

router = APIRouter(prefix='/todo', tags=['todo'])


@router.get('/')
def get_all_todos(session: Session = Depends(get_db_session)) -> list[TodoDto]:
    return [to_todo_dto(entity) for entity in list_todos(session)]


@router.get('/{id}', response_model=TodoDto)
def get_todo(id: int, session: Session = Depends(get_db_session)):
    entity = get_todo_by_id(session, id)
    return to_todo_dto(entity) if entity else Response(status_code=404, content='not found')


@router.post('/', status_code=201, response_model=TodoDto)
def post_todo(dto: TodoPostDto, response: Response, session: Session = Depends(get_db_session)) -> TodoDto:
    entity = create_todo(session, dto)
    add_categories_to_todo(session, entity.todo_id, *dto.categories)
    response.headers['Location'] = f'/todo/{entity.todo_id}'
    return to_todo_dto(entity)


@router.put('/{id}', response_model=TodoDto)
def put_todo(id: int, dto: TodoPutDto, session: Session = Depends(get_db_session)) -> TodoDto:
    return to_todo_dto(update_todo(session, id, dto))


@router.patch('/{id}', response_model=TodoDto)
def patch_todo_status(id: int, dto: TodoPatchDto, session: Session = Depends(get_db_session)):
    entity = get_todo_by_id(session, id)
    if entity and entity.is_done != dto.done:
        entity = toggle_todo(session, id)
    return to_todo_dto(entity) if entity else Response(status_code=404, content='not found')


@router.delete('/{id}', status_code=204)
def remove_todo(id: int, session: Session = Depends(get_db_session)):
    delete_todo(session, id)


@router.patch('/{id}/category')
def update_todo_categories(id: int, body: dict, session: Session = Depends(get_db_session)):
    entity = add_categories_to_todo(session, id, *body['categories'])
    return to_todo_dto(entity)


