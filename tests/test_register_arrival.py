from dataclasses import dataclass
import pytest

from products.application.register_arrival import RegisterArrivalUsecase, ArrivalDTO
from products.domain.exceptions.product_not_found import ProductNotFoundException
from tests.mocks import MockLogger, MockProductRepository
from tests.mothers.product import ProductMother


@dataclass
class RegisterArrivalSetup:
    usecase: RegisterArrivalUsecase
    repo: MockProductRepository


@pytest.fixture
def register_arrival_setup() -> RegisterArrivalSetup:
    repo = MockProductRepository()
    usecase = RegisterArrivalUsecase(MockLogger(), repo)
    return RegisterArrivalSetup(usecase, repo)


def test_happy_path(mock_user, register_arrival_setup: RegisterArrivalSetup):
    product = ProductMother.create(stock=10)
    register_arrival_setup.repo.save(product)

    register_arrival_setup.usecase.run(mock_user, ArrivalDTO(product.id, 2))
    product_after_arrival = register_arrival_setup.repo.get_by_id(product.id)

    assert product_after_arrival is not None
    assert product_after_arrival.stock == 12
    assert register_arrival_setup.repo.get_count() == 1


def test_registering_arrival_for_non_existing_product_fails(
    mock_user, register_arrival_setup: RegisterArrivalSetup
):
    with pytest.raises(ProductNotFoundException):
        register_arrival_setup.usecase.run(mock_user, ArrivalDTO("irrelevant-id", 1))
