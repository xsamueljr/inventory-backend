from typing import Dict

from products.domain.dtos.update_product import UpdateProductDTO
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product import Product
from products.domain.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):

    def __init__(self) -> None:
        self.__products: Dict[str, Product] = {}

    def save(self, product: Product) -> None:
        self.__products[product.id] = product
    
    def get_by_id(self, id: str) -> Product | None:
        return self.__products.get(id)
    
    def get_by_name(self, name: str) -> Product | None:
        for product in self.__products.values():
            if product.model == name:
                return product
        return None
    
    def update(self, id: str, input: UpdateProductDTO) -> Product:
        product = self.get_by_id(id)
        if not product:
            raise ProductNotFoundException(id)
        
        if input.model:
            product.model = input.model
        if input.color:
            product.color = input.color
        if input.arriving_date:
            product.arriving_date = input.arriving_date
        if input.stock:
            product.stock = input.stock
        
        return product