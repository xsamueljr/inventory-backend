from typing import List

from products.application.dtos.public_product import PublicProductInfo
from products.domain.product_repository import ProductRepository


class GetAllProductsUsecase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.__repo = product_repository

    def run(self) -> List[PublicProductInfo]:
        return [PublicProductInfo.from_domain(product) for product in self.__repo.get_all()]
