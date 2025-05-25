from dataclasses import dataclass

import pytest

from tests.mocks import MockLogger, MockMailer, MockProductRepository
from products.application.create_product import CreateProductUseCase
from products.application.dtos.create_product import CreateProductDTO


@dataclass
class CreateProductSetup:
    usecase: CreateProductUseCase
    repo: MockProductRepository
    mailer: MockMailer


@pytest.fixture
def create_product_setup() -> CreateProductSetup:
    repo = MockProductRepository()
    mailer = MockMailer()
    usecase = CreateProductUseCase(MockLogger(), repo, mailer)

    return CreateProductSetup(usecase, repo, mailer)


def test_happy_path(create_product_setup: CreateProductSetup, mock_user):
    input = CreateProductDTO("Sofá beisbol")

    id = create_product_setup.usecase.run(mock_user, input)

    assert id is not None
    assert create_product_setup.mailer.was_called_once()
    assert create_product_setup.repo.get_count() == 1
