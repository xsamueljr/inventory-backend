from typing import List

from products.application.dtos.public_product import PublicProductInfo
from products.domain.product_repository import ProductRepository


class SearchProductsByNameUsecase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.__product_repository = product_repository

    def run(self, name: str) -> List[PublicProductInfo]:
        products = self.__product_repository.search_by_name(name)
        return [PublicProductInfo.from_domain(product) for product in products]
