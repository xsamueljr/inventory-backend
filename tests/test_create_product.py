from typing import Tuple

import pytest

from tests.mocks import mock_mailer, MockMailer, mock_product_repository, MockProductRepository
from emails.domain.email import Email
from emails.domain.emailer import Emailer
from products.application.create_product import CreateProductUseCase
from products.application.dtos.create_product import CreateProductDTO
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository


@pytest.fixture
def use_case_and_dependencies(mock_mailer, mock_product_repository) -> Tuple[CreateProductUseCase, MockMailer, MockProductRepository]:
    usecase = CreateProductUseCase(
        mock_product_repository,
        mock_mailer
    )
    
    return (usecase, mock_mailer, mock_product_repository)


def test_happy_path(use_case_and_dependencies):
    use_case, mailer, repo = use_case_and_dependencies

    input = CreateProductDTO("Sofá beisbol", "Blanco")

    id = use_case.run(input)

    assert id is not None
    assert mailer.was_called_once()
    assert len(repo.get_all()) == 1
