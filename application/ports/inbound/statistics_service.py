from abc import ABC, abstractmethod

from domain.models.statistics import ReminderStatistics


class StatisticsService(ABC):
    @abstractmethod
    def get_statistics(self) -> ReminderStatistics: ...

