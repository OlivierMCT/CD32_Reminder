from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from features.shared.db import get_db_session
from features.category.schemas import CategoryDto, CategoryPostDto, CategoryPutDto
from features.category.slice import (
    create_category,
    delete_category,
    get_category_by_id,
    list_categories,
    to_category_dto,
    update_category,
)

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/')
def get_all_categories(session: Session = Depends(get_db_session)) -> list[CategoryDto]:
    return [to_category_dto(entity) for entity in list_categories(session)]


@router.get('/{id}', response_model=CategoryDto)
def get_category(id: int, session: Session = Depends(get_db_session)):
    entity = get_category_by_id(session, id)
    return to_category_dto(entity) if entity else Response(status_code=404, content='not found')


@router.post('/', status_code=201, response_model=CategoryDto)
def post_category(dto: CategoryPostDto, response: Response, session: Session = Depends(get_db_session)) -> CategoryDto:
    entity = create_category(session, dto)
    response.headers['Location'] = f'/category/{entity.category_id}'
    return to_category_dto(entity)


@router.put('/{id}', response_model=CategoryDto)
def put_category(id: int, dto: CategoryPutDto, session: Session = Depends(get_db_session)) -> CategoryDto:
    return to_category_dto(update_category(session, id, dto))


@router.delete('/{id}', status_code=204)
def remove_category(id: int, session: Session = Depends(get_db_session)):
    delete_category(session, id)


