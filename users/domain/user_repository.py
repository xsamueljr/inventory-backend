from abc import ABC, abstractmethod
from typing import Optional

from users.domain.user import User


class UserRepository(ABC):
    
    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[User]: ...