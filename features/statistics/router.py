from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from features.shared.db import get_db_session
from features.statistics.schemas import ReminderStatisticsDto
from features.statistics.slice import get_statistics

router = APIRouter(prefix='/statistics', tags=['statistics'])


@router.get('/', response_model=ReminderStatisticsDto)
def fetch_statistics(session: Session = Depends(get_db_session)) -> ReminderStatisticsDto:
    return get_statistics(session)


