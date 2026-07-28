from enum import Enum, auto


class ErrorType(Enum):
    NOT_FOUND = auto()
    CONFLICT = auto()
    UNAUTHORIZED = auto()
    VALIDATION = auto()
    INTERNAL = auto()


class AppException(Exception):
    def __init__(self, *args: object, is_operational: bool, type: ErrorType) -> None:
        super().__init__(*args)
        self.is_operational = is_operational
        self.type = type
