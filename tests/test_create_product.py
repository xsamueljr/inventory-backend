from dataclasses import dataclass

import pytest

from activity.infrastructure.in_memory_record_repository import InMemoryRecordRepository
from tests.mocks import MockLogger, MockMailer, MockProductRepository
from products.application.create_product import CreateProductUseCase
from products.application.dtos.create_product import CreateProductDTO


@dataclass
class CreateProductSetup:
    usecase: CreateProductUseCase
    product_repo: MockProductRepository
    record_repo: InMemoryRecordRepository
    mailer: MockMailer


@pytest.fixture
def create_product_setup() -> CreateProductSetup:
    product_repo = MockProductRepository()
    record_repo = InMemoryRecordRepository()
    mailer = MockMailer()
    usecase = CreateProductUseCase(MockLogger(), product_repo, record_repo, mailer)

    return CreateProductSetup(usecase, product_repo, record_repo, mailer)


def test_happy_path(create_product_setup: CreateProductSetup, mock_user):
    input = CreateProductDTO("Sofá beisbol")

    id = create_product_setup.usecase.run(mock_user, input)

    assert id is not None
    assert create_product_setup.mailer.was_called_once()
    assert create_product_setup.product_repo.get_count() == 1
