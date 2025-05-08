from dataclasses import dataclass

import pytest

from tests.mocks import mock_mailer, MockMailer, mock_product_repository, MockProductRepository
from emails.domain.email import Email
from emails.domain.emailer import Emailer
from products.application.create_product import CreateProductUseCase
from products.application.dtos.create_product import CreateProductDTO
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository


@dataclass
class CreateProductSetup:
    usecase: CreateProductUseCase
    repo: MockProductRepository
    mailer: MockMailer


@pytest.fixture
def create_product_setup(mock_mailer, mock_product_repository) -> CreateProductSetup:
    usecase = CreateProductUseCase(
        mock_product_repository,
        mock_mailer
    )

    return CreateProductSetup(usecase, mock_product_repository, mock_mailer)


def test_happy_path(create_product_setup: CreateProductSetup):
    input = CreateProductDTO("Sofá beisbol", "Blanco")

    id = create_product_setup.usecase.run(input)

    assert id is not None
    assert create_product_setup.mailer.was_called_once()
    assert len(create_product_setup.repo.get_all()) == 1
