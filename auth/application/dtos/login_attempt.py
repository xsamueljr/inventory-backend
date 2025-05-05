from dataclasses import dataclass


@dataclass(frozen=True)
class LoginAttemptDTO:
    username: str
    password: str