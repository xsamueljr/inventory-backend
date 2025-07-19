from typing import List

from fastapi import APIRouter, Depends

from activity.application.dtos.public_record_info import PublicRecordInfo
from auth.domain.logged_user_info import LoggedUserInfo
from core.infrastructure.fastapi.security import get_current_user
from activity.application.get_own_records import GetOwnRecordsUseCase
from activity.infrastructure.fastapi.dependencies import get_own_records_usecase
from shared.infrastructure.fastapi.dtos import PaginationQueryParams

router = APIRouter(prefix="/api/records", tags=["records"])


@router.get("/own")
def get_own_records(
    user: LoggedUserInfo = Depends(get_current_user),
    usecase: GetOwnRecordsUseCase = Depends(get_own_records_usecase),
    pagination: PaginationQueryParams = Depends(),
) -> List[PublicRecordInfo]:
    return usecase.run(user, pagination.limit, pagination.offset)
