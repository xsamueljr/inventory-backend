from typing import List
from activity.domain.record import Record
from activity.domain.record_repository import RecordRepository
from auth.domain.logged_user_info import LoggedUserInfo


class GetOwnRecordsUseCase:
    def __init__(self, repo: RecordRepository) -> None:
        self.__repo = repo

    def run(self, user: LoggedUserInfo, limit: int, offset: int) -> List[Record]:
        return self.__repo.get_by_user_id(user.id, limit, offset)
