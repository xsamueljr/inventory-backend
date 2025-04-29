from shared.domain.exception import AppException


class EmailError(AppException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, is_operational=True)
