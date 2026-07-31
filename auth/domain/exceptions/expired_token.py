from shared.domain.exception import AppException, ErrorType


class ExpiredTokenException(AppException):
    def __init__(self) -> None:
        super().__init__(
            "Token is expired", is_operational=True, type=ErrorType.UNAUTHORIZED
        )
