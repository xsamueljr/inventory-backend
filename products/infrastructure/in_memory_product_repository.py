from typing import Dict, List

from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product import Product
from products.domain.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):

    def __init__(self) -> None:
        self.__products: Dict[str, Product] = {}

    def save(self, product: Product) -> None:
        self.__products[product.id] = product
    
    def get_all(self) -> List[Product]:
        return list(self.__products.values())
    
    def get_by_id(self, id: str) -> Product | None:
        return self.__copy(self.__products.get(id))
    
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
    
    def __copy(self, product: Product | None) -> Product | None:
        if not product:
            return None
        
        return Product(
            product.name,
            product.stock,
            product.arriving_date,
            product.id
        )