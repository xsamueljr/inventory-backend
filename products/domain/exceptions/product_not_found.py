from shared.domain.exception import AppException


class ProductNotFoundException(AppException):
    def __init__(self, id: str | None = None) -> None:
        if id:
            message = f"There is no product with id {id}"
        else:
            message = "Product not found"

        super().__init__(message, is_operational=True)
