from typing import Dict
from users.domain.user import User, UserRole
from users.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.__users: Dict[str, User] = {}

    def save(self, user: User) -> None:
        self.__users[user.id] = user

    def get_by_id(self, id: str) -> User | None:
        user = self.__users.get(id)
        if user is None:
            return None
        return User(
            id=user.id,
            username=user.username,
            password=user.password,
            shop_name=user.shop_name,
            location_id=user.location_id,
            role=user.role if user.role is not None else UserRole.USER,
        )

    def get_by_username(self, username: str) -> User | None:
        for user in self.__users.values():
            if user.username == username:
                return User(
                    id=user.id,
                    username=user.username,
                    password=user.password,
                    shop_name=user.shop_name,
                    location_id=user.location_id,
                    role=user.role if user.role is not None else UserRole.USER,
                )
        return None

