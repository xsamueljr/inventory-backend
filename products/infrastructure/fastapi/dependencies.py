from functools import lru_cache

from fastapi import Depends

from core.infrastructure.fastapi.dependencies import get_mailer
from emails.domain.emailer import Emailer
from products.application.create_product import CreateProductUseCase
from products.application.delete_by_id import DeleteProductByIdUsecase
from products.application.get_all import GetAllProductsUsecase
from products.application.get_by_id import GetProductByIdUsecase
from products.application.register_arrival import RegisterArrivalUsecase
from products.application.register_sell import RegisterSaleUsecase
from products.domain.product_repository import ProductRepository
from products.infrastructure.sqlite_product_repository import SQLiteProductRepository
from products.infrastructure.supabase_product_repository import SupabaseProductRepository
from shared.infrastructure.env import env
from shared.infrastructure.basic_logger import basic_logger

@lru_cache
def get_product_repository() -> ProductRepository:
    if env.SQLITE_PATH:
        return SQLiteProductRepository(env.SQLITE_PATH)
    return SupabaseProductRepository()


def get_create_product_usecase(
        product_repository: ProductRepository = Depends(get_product_repository),
        mailer: Emailer = Depends(get_mailer)
) -> CreateProductUseCase:
    return CreateProductUseCase(basic_logger, product_repository, mailer)

def get_register_sale_usecase(
        product_repository: ProductRepository = Depends(get_product_repository),
        mailer: Emailer = Depends(get_mailer)
) -> RegisterSaleUsecase:
    return RegisterSaleUsecase(product_repository, mailer, basic_logger)

def get_register_arrival_usecase(
        product_repository: ProductRepository = Depends(get_product_repository)
) -> RegisterArrivalUsecase:
    return RegisterArrivalUsecase(basic_logger, product_repository)

def get_all_products_usecase(repo: ProductRepository = Depends(get_product_repository)) -> GetAllProductsUsecase:
    return GetAllProductsUsecase(repo)

def get_product_by_id_usecase(repo: ProductRepository = Depends(get_product_repository)) -> GetProductByIdUsecase:
    return GetProductByIdUsecase(repo)

def get_delete_product_usecase(repo: ProductRepository = Depends(get_product_repository)) -> DeleteProductByIdUsecase:
    return DeleteProductByIdUsecase(basic_logger, repo)
