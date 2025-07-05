from dataclasses import dataclass

import pytest

from activity.infrastructure.in_memory_record_repository import InMemoryRecordRepository
from products.application.register_arrival import RegisterArrivalUsecase, ArrivalDTO
from products.domain.exceptions.product_not_found import ProductNotFoundException
from tests.mocks import MockLogger, MockProductRepository
from tests.mothers.product import ProductMother


@dataclass
class RegisterArrivalSetup:
    usecase: RegisterArrivalUsecase
    product_repo: MockProductRepository
    record_repo: InMemoryRecordRepository


@pytest.fixture
def register_arrival_setup() -> RegisterArrivalSetup:
    product_repo = MockProductRepository()
    record_repo = InMemoryRecordRepository()
    usecase = RegisterArrivalUsecase(MockLogger(), product_repo, record_repo)
    return RegisterArrivalSetup(usecase, product_repo, record_repo)


def test_happy_path(mock_user, register_arrival_setup: RegisterArrivalSetup):
    product = ProductMother.create(stock=10)
    register_arrival_setup.product_repo.save(product)

    register_arrival_setup.usecase.run(mock_user, ArrivalDTO(product.id, 2))
    product_after_arrival = register_arrival_setup.product_repo.get_by_id(product.id)

    assert product_after_arrival is not None
    assert product_after_arrival.stock == 12
    assert register_arrival_setup.product_repo.get_count() == 1


def test_registering_arrival_for_non_existing_product_fails(
    mock_user, register_arrival_setup: RegisterArrivalSetup
):
    with pytest.raises(ProductNotFoundException):
        register_arrival_setup.usecase.run(mock_user, ArrivalDTO("irrelevant-id", 1))
