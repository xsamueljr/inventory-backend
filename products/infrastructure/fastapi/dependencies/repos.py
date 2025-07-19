from products.domain.product_repository import ProductRepository
from products.infrastructure.sqlite_product_repository import SQLiteProductRepository
from products.infrastructure.supabase_product_repository import (
    SupabaseProductRepository,
)
from shared.infrastructure.env import ENV


from functools import lru_cache


@lru_cache
def get_product_repository() -> ProductRepository:
    if ENV.SQLITE_PATH:
        return SQLiteProductRepository(ENV.SQLITE_PATH)
    return SupabaseProductRepository()
