from functools import lru_cache

from users.domain.user_repository import UserRepository
from shared.infrastructure.env import env
from users.infrastructure.sqlite_user_repository import SQLiteUserRepository
from users.infrastructure.supabase_user_repository import SupabaseUserRepository


@lru_cache
def get_user_repository() -> UserRepository:
    if env.SQLITE_PATH:
        return SQLiteUserRepository(env.SQLITE_PATH)
    return SupabaseUserRepository()
