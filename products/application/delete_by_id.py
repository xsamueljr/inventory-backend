from products.domain.product_repository import ProductRepository


class DeleteProductByIdUsecase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.__repo = product_repository

    def run(self, id: str) -> None:
        self.__repo.delete(id)
