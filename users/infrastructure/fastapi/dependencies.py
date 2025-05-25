from functools import lru_cache

from users.domain.user_repository import UserRepository
from shared.infrastructure.env import ENV
from users.infrastructure.sqlite_user_repository import SQLiteUserRepository
from users.infrastructure.supabase_user_repository import SupabaseUserRepository


@lru_cache
def get_user_repository() -> UserRepository:
    if ENV.SQLITE_PATH:
        return SQLiteUserRepository(ENV.SQLITE_PATH)
    return SupabaseUserRepository()
