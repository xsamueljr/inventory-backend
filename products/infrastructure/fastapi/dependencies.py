from functools import lru_cache

from fastapi import Depends

from core.infrastructure.fastapi.dependencies import get_mailer
from emails.domain.emailer import Emailer
from products.application.create_product import CreateProductUseCase
from products.application.get_all import GetAllProductsUsecase
from products.application.get_by_id import GetProductByIdUsecase
from products.application.register_sell import RegisterSaleUsecase
from products.domain.product_repository import ProductRepository
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository


@lru_cache
def get_product_repository() -> ProductRepository:
    return InMemoryProductRepository()


def get_create_product_usecase(
        product_repository: ProductRepository = Depends(get_product_repository),
        mailer: Emailer = Depends(get_mailer)
) -> CreateProductUseCase:
    return CreateProductUseCase(product_repository, mailer)

def get_register_sale_usecase(
        product_repository: ProductRepository = Depends(get_product_repository),
        mailer: Emailer = Depends(get_mailer)
) -> RegisterSaleUsecase:
    return RegisterSaleUsecase(product_repository, mailer)

def get_all_products_usecase(repo: ProductRepository = Depends(get_product_repository)) -> GetAllProductsUsecase:
    return GetAllProductsUsecase(repo)

def get_product_by_id_usecase(repo: ProductRepository = Depends(get_product_repository)) -> GetProductByIdUsecase:
    return GetProductByIdUsecase(repo)
