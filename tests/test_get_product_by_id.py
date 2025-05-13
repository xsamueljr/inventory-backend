from dataclasses import dataclass
from uuid import uuid4

import pytest

from products.application.dtos.public_product import PublicProductInfo
from products.application.get_by_id import GetProductByIdUsecase
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository
from products.infrastructure.sqlite_product_repository import SQLiteProductRepository
from shared.infrastructure.sqlite_connection import get_connection
from tests.mothers.product import ProductMother


@dataclass
class GetProductByIdSetup:
    repo: ProductRepository
    usecase: GetProductByIdUsecase


@pytest.fixture
def get_product_setup() -> GetProductByIdSetup:
    repo = SQLiteProductRepository("test.db")
    usecase = GetProductByIdUsecase(repo)
    return GetProductByIdSetup(repo, usecase)


@pytest.mark.parametrize("id", ("id1", "id2", "id3"))
def test_it_works(id: str, get_product_setup: GetProductByIdSetup) -> None:
    product = ProductMother.create(id=id)
    get_product_setup.repo.save(product)

    retrieved_product = get_product_setup.usecase.run(product.id)

    assert isinstance(retrieved_product, PublicProductInfo)
    assert product.id == retrieved_product.id
    assert product.name == retrieved_product.name
    assert product.stock == retrieved_product.stock


def test_throws_exception_if_not_found(get_product_setup: GetProductByIdSetup) -> None:
    with pytest.raises(ProductNotFoundException):
        get_product_setup.usecase.run(str(uuid4()))
