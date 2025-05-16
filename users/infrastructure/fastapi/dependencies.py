from functools import lru_cache

from users.domain.user_repository import UserRepository
from users.infrastructure.in_memory_user_repository import InMemoryUserRepository
from shared.infrastructure.env import env
from users.infrastructure.sqlite_user_repository import SQLiteUserRepository

@lru_cache
def get_user_repository() -> UserRepository:
    if env.SQLITE_PATH:
        return SQLiteUserRepository(env.SQLITE_PATH)
    return InMemoryUserRepository()
