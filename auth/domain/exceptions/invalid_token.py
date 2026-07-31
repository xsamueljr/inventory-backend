from shared.domain.exception import AppException, ErrorType


class InvalidTokenException(AppException):
    def __init__(self) -> None:
        super().__init__(
            "Token is invalid", is_operational=True, type=ErrorType.UNAUTHORIZED
        )
