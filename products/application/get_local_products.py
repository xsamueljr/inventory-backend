from products.application.dtos.public_product import PublicProductInfo
from products.domain.product_repository import ProductRepository


class GetLocalProductsUseCase:
    def __init__(self, repo: ProductRepository):
        self.__repo = repo

    def run(self, location_id: int, limit: int, offset: int) -> list[PublicProductInfo]:
        products = self.__repo.get_by_location(location_id, limit, offset)
        return [PublicProductInfo.from_domain(p) for p in products]
