from typing import Dict, List
from activity.domain.record import Record
from activity.domain.record_repository import RecordRepository


class InMemoryRecordRepository(RecordRepository):
    def __init__(self) -> None:
        self.__records: Dict[str, Record] = {}

    def save(self, record: Record) -> None:
        self.__records[record.id] = record

    def get_all(self, limit: int, offset: int) -> List[Record]:
        return list(self.__records.values())

    def get_by_user_id(self, id: str, limit: int, offset: int) -> List[Record]:
        return [record for record in self.__records.values() if record.user_id == id]
