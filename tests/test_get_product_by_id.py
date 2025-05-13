from dataclasses import dataclass
from typing import Tuple

import pytest

from products.application.dtos.public_product import PublicProductInfo
from products.application.get_by_id import GetProductByIdUsecase
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository
from tests.mothers.product import ProductMother


@dataclass
class GetProductByIdSetup:
    repo: InMemoryProductRepository
    usecase: GetProductByIdUsecase


ID_EXAMPLES: Tuple[str, ...] = ("id1", "id2", "id3")

@pytest.fixture
def get_product_setup() -> GetProductByIdSetup:
    repo = InMemoryProductRepository()
    usecase = GetProductByIdUsecase(repo)
    return GetProductByIdSetup(repo, usecase)


@pytest.mark.parametrize("id", ID_EXAMPLES)
def test_it_works(id: str, get_product_setup: GetProductByIdSetup) -> None:
    product = ProductMother.create(id=id)
    get_product_setup.repo.save(product)

    retrieved_product = get_product_setup.usecase.run(product.id)

    assert isinstance(retrieved_product, PublicProductInfo)
    assert product.id == retrieved_product.id
    assert product.name == retrieved_product.name
    assert product.stock == retrieved_product.stock


@pytest.mark.parametrize("id", ID_EXAMPLES)
def test_throws_exception_if_not_found(id: str, get_product_setup: GetProductByIdSetup) -> None:
    with pytest.raises(ProductNotFoundException):
        get_product_setup.usecase.run(id)
