from typing import Dict
from users.domain.user import User
from users.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    
    def __init__(self) -> None:
        self.__users: Dict[str, User] = {}
    
    def save(self, user: User) -> None:
        self.__users[user.id] = user
    
    def get_by_id(self, id: str) -> User | None:
        return self.__users.get(id)
    
    def get_by_username(self, username: str) -> User | None:
        print(len(self.__users))
        for user in self.__users.values():
            if user.username == username:
                return user
        return None
