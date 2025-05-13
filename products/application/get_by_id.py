from products.application.dtos.public_product import PublicProductInfo
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository


class GetProductByIdUsecase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.__repo = product_repository
    
    def run(self, id: str) -> PublicProductInfo:
        product = self.__repo.get_by_id(id)
        if not product:
            raise ProductNotFoundException(id)
        
        return PublicProductInfo.from_domain(product)
