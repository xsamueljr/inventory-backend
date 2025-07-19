from abc import ABC, abstractmethod
from typing import List

from activity.domain.record import Record


class RecordRepository(ABC):
    @abstractmethod
    def save(self, record: Record) -> None: ...

    @abstractmethod
    def get_all(self, limit: int, offset: int) -> List[Record]: ...

    @abstractmethod
    def get_by_user_id(self, id: str, limit: int, offset: int) -> List[Record]: ...
