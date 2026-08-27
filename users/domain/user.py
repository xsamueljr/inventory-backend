from dataclasses import dataclass
from enum import Enum


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass
class User:
    id: str
    username: str
    password: str
    shop_name: str
    location_id: int | None = None
    role: UserRole = UserRole.USER

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
