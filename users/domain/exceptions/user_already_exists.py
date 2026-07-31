from shared.domain.exception import AppException, ErrorType


class UserAlreadyExistsException(AppException):
    def __init__(self, id: str) -> None:
        super().__init__(
            f"There's already a user with ID {id}",
            is_operational=True,
            type=ErrorType.CONFLICT,
        )
