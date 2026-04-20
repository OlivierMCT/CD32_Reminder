from fastapi import APIRouter, Depends

from application.ports.inbound.statistics_service import StatisticsService
from domain.models.statistics import ReminderStatistics
from presentation.api.schemas.statistics import (
    CategoryStatisticsDto,
    ReminderStatisticsDto,
    StatusStatisticsDto,
)

router = APIRouter(prefix='/statistics', tags=['statistics'])


def get_statistics_service() -> StatisticsService:
    raise NotImplementedError("This is a placeholder for the actual dependency injection of StatisticsService")


@router.get('/', response_model=ReminderStatisticsDto)
def get_statistics(service: StatisticsService = Depends(get_statistics_service)) -> ReminderStatisticsDto:
    return to_dto_from_model(service.get_statistics())


def to_dto_from_model(model: ReminderStatistics) -> ReminderStatisticsDto:
    return ReminderStatisticsDto(
        total_todos=model.total_todos,
        by_status=[
            StatusStatisticsDto(
                status=item.status,
                count=item.count,
                percentage=item.percentage,
            )
            for item in model.by_status
        ],
        by_category=[
            CategoryStatisticsDto(
                category_id=item.category_id,
                title=item.title,
                count=item.count,
                percentage=item.percentage,
            )
            for item in model.by_category
        ],
    )

