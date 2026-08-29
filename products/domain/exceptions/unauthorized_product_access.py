from shared.domain.exception import AppException, ErrorType


class UnauthorizedProductAccess(AppException):
    def __init__(self, product_id: str) -> None:
        super().__init__(f"Unauthorized access to product {product_id}", is_operational=True, type=ErrorType.UNAUTHORIZED)
