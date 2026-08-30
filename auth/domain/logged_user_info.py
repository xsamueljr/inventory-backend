from dataclasses import dataclass

from users.domain.user import User


@dataclass(frozen=True)
class LoggedUserInfo:
    id: str
    name: str
    location_id: int
    is_admin: bool = False

    @classmethod
    def from_domain(cls, user: User) -> "LoggedUserInfo":
        return cls(
            id=user.id,
            name=user.username,
            location_id=user.location_id,
            is_admin=user.is_admin(),
        )
