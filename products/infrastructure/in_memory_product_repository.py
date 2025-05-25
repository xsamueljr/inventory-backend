from typing import Dict, List

from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product import Product
from products.domain.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self) -> None:
        self.__products: Dict[str, Product] = {}

    def save(self, product: Product) -> None:
        self.__products[product.id] = product

    def get_all(self, limit: int, offset: int) -> List[Product]:
        return list(self.__products.values())[offset : offset + limit]

    def get_by_id(self, id: str) -> Product | None:
        product = self.__products.get(id)
        if not product:
            return None
        return self.__copy(product)

    def get_by_name(self, name: str) -> Product | None:
        for product in self.__products.values():
            if product.name == name:
                return self.__copy(product)
        return None

    def update(self, product: Product) -> None:
        existing_product = self.get_by_id(product.id)
        if not existing_product:
            raise ProductNotFoundException(product.id)

        self.__products[existing_product.id] = product

    def delete(self, id: str) -> None:
        self.__products.pop(id, None)

    def search_by_name(self, name: str) -> List[Product]:
        search_term = name.lower()

        return [
            self.__copy(product)
            for product in self.__products.values()
            if search_term in product.name.lower()
        ]

    def __copy(self, product: Product) -> Product:
        return Product(product.name, product.stock, product.arriving_date, product.id)
