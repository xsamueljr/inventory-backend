from dataclasses import dataclass

import pytest

from activity.domain.record import RecordKind
from products.application.delete_by_id import DeleteProductByIdUsecase
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.infrastructure.in_memory_product_repository import (
    InMemoryProductRepository,
)
from activity.infrastructure.in_memory_record_repository import InMemoryRecordRepository
from tests.mocks import MockLogger
from tests.mothers.product import ProductMother
from auth.domain.logged_user_info import LoggedUserInfo


@dataclass
class DeleteProductSetup:
    product_repo: InMemoryProductRepository
    record_repo: InMemoryRecordRepository
    usecase: DeleteProductByIdUsecase


@pytest.fixture
def delete_product_setup() -> DeleteProductSetup:
    product_repo = InMemoryProductRepository()
    record_repo = InMemoryRecordRepository()
    usecase = DeleteProductByIdUsecase(MockLogger(), product_repo, record_repo)
    return DeleteProductSetup(product_repo, record_repo, usecase)


def test_deleting_product_that_does_not_exist_fails(
    delete_product_setup: DeleteProductSetup, mock_user: LoggedUserInfo
):
    with pytest.raises(ProductNotFoundException):
        delete_product_setup.usecase.run(mock_user, "irrelevant-id")


def test_product_is_not_found_after_deleting_it(
    delete_product_setup: DeleteProductSetup, mock_user: LoggedUserInfo
):
    product = ProductMother.create()
    delete_product_setup.product_repo.save(product)

    delete_product_setup.usecase.run(mock_user, product.id)

    after_delete = delete_product_setup.product_repo.get_by_id(product.id)

    assert after_delete is None


def test_deleting_a_product_successfully_creates_a_record(
    delete_product_setup: DeleteProductSetup, mock_user: LoggedUserInfo
):
    product = ProductMother.create()
    delete_product_setup.product_repo.save(product)

    delete_product_setup.usecase.run(mock_user, product.id)

    records = delete_product_setup.record_repo.get_all(limit=10, offset=0)

    assert len(records) == 1
    assert records[0].kind == RecordKind.PRODUCT_DELETED
