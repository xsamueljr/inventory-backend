from functools import lru_cache

from fastapi import Depends

from activity.infrastructure.sqlite_record_repository import SQLiteRecordRepository
from activity.infrastructure.supabase_record_repository import SupabaseRecordRepository
from activity.domain.record_repository import RecordRepository
from activity.application.get_own_records import GetOwnRecordsUseCase
from products.domain.product_repository import ProductRepository
from shared.infrastructure.env import ENV
from users.domain.user_repository import UserRepository
from products.infrastructure.fastapi.dependencies.repos import get_product_repository
from users.infrastructure.fastapi.dependencies import get_user_repository


@lru_cache
def get_record_repository() -> RecordRepository:
    if ENV.SQLITE_PATH:
        return SQLiteRecordRepository(ENV.SQLITE_PATH)
    return SupabaseRecordRepository()


def get_own_records_usecase(
    record_repository: RecordRepository = Depends(get_record_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetOwnRecordsUseCase:
    return GetOwnRecordsUseCase(record_repository, product_repository, user_repository)
