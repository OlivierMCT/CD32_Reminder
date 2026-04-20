from fastapi import APIRouter, Depends, Response

from application.ports.inbound.category_service import CategoryService
from domain.models.category import Category, CategoryNew, CategoryUpdate
from presentation.api.schemas.category import CategoryDto, CategoryPostDto, CategoryPutDto

router = APIRouter(prefix='/category', tags=['category'])


def get_category_service() -> CategoryService:
	raise NotImplementedError("This is a placeholder for the actual dependency injection of CategoryService")


@router.get('/')
def get_all_categories(service: CategoryService = Depends(get_category_service)) -> list[CategoryDto]:
	return [to_dto_from_model(m) for m in service.find_all()]


@router.get('/{id}', response_model=CategoryDto)
def get_category(id: int, service: CategoryService = Depends(get_category_service)):
	model = service.find_by_id(id)
	return to_dto_from_model(model) if model else Response(status_code=404, content='not found')


@router.post('/', status_code=201, response_model=CategoryDto)
def post_category(dto: CategoryPostDto, response: Response,
				  service: CategoryService = Depends(get_category_service)) -> CategoryDto:
	model = service.save_new(to_model_from_postdto(dto))
	response.headers['Location'] = f'/category/{model.id}'
	return to_dto_from_model(model)


@router.put('/{id}', response_model=CategoryDto)
def put_category(id: int, dto: CategoryPutDto, service: CategoryService = Depends(get_category_service)) -> CategoryDto:
	model = service.save_update(to_model_from_putdto(id, dto))
	return to_dto_from_model(model)


@router.delete('/{id}', status_code=204)
def delete_category(id: int, service: CategoryService = Depends(get_category_service)):
	service.remove(id)


def to_dto_from_model(model: Category) -> CategoryDto:
	return CategoryDto(
		id=model.id,
		title=model.title,
		color=model.color,
		todo_count=model.todo_count,
		todo_done=model.todo_done,
		progress_rate=model.progress_rate,
	)


def to_model_from_postdto(dto: CategoryPostDto) -> CategoryNew:
	return CategoryNew(
		title=dto.title,
		color=dto.color,
	)


def to_model_from_putdto(id: int, dto: CategoryPutDto) -> CategoryUpdate:
	return CategoryUpdate(
		id=id,
		title=dto.title,
		color=dto.color,
	)

