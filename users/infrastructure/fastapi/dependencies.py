from functools import lru_cache

from users.domain.user_repository import UserRepository
from users.infrastructure.in_memory_user_repository import InMemoryUserRepository


@lru_cache
def get_user_repository() -> UserRepository:
    return InMemoryUserRepository()
