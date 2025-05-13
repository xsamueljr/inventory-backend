from shared.domain.exception import AppException


class ProductAlreadyExistsException(AppException):
    def __init__(
            self,
            *,
            id: str | None = None,
            name: str | None = None
    ) -> None:
        if id:
            message = f"There's already a product with ID {id}"
        elif name:
            message = f"There's already a product with name {name}"
        else:
            message = "Product already exists"

        super().__init__(message, is_operational=True)
