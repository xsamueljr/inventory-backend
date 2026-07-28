from shared.domain.exception import AppException, ErrorType


class InvalidCredentialsException(AppException):
    def __init__(self) -> None:
        super().__init__("Invalid credentials", is_operational=True, type=ErrorType.UNAUTHORIZED)
