from functools import lru_cache

from shared.infrastructure.database_credentials import DatabaseCredentials
from shared.infrastructure.env import ENV
from users.domain.user_repository import UserRepository
from users.infrastructure.sqlite_user_repository import SQLiteUserRepository
from users.infrastructure.supabase_user_repository import SupabaseUserRepository


@lru_cache
def get_user_repository() -> UserRepository:
    if ENV.SQLITE_PATH:
        return SQLiteUserRepository(ENV.SQLITE_PATH)
    return SupabaseUserRepository(
        DatabaseCredentials(
            connection_string=ENV.SUPABASE_PG_CONN,
            schema=ENV.PG_SCHEMA,
        )
    )
