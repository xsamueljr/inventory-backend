from shared.domain.exception import AppException, ErrorType


class EmailError(AppException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, is_operational=False, type=ErrorType.INTERNAL)
