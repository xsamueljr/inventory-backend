from dataclasses import dataclass


@dataclass(frozen=True)
class LoggedUserInfo:
    id: str
    name: str
