from dataclasses import dataclass

import pytest

from products.application.delete_by_id import DeleteProductByIdUsecase
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository
from tests.mocks import MockLogger
from tests.mothers.product import ProductMother


@dataclass
class DeleteProductSetup:
    repo: InMemoryProductRepository
    usecase: DeleteProductByIdUsecase


@pytest.fixture
def delete_product_setup() -> DeleteProductSetup:
    repo = InMemoryProductRepository()
    usecase = DeleteProductByIdUsecase(
        MockLogger(),
        repo
    )
    return DeleteProductSetup(repo, usecase)


def test_deleting_product_that_does_not_exist_fails(
        delete_product_setup,
        mock_user
):
    with pytest.raises(ProductNotFoundException):
        delete_product_setup.usecase.run(mock_user, "irrelevant-id")


def test_product_is_not_found_after_deleting_it(
        delete_product_setup,
        mock_user
):
    product = ProductMother.create()
    delete_product_setup.repo.save(product)

    delete_product_setup.usecase.run(mock_user, product.id)

    after_delete = delete_product_setup.repo.get_by_id(product.id)

    assert after_delete is None
