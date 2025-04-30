from typing import Tuple

import pytest

from products.application.register_sell import RegisterSaleUsecase
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository
from tests.mocks import MockMailer
from tests.mothers.product import ProductMother

@pytest.fixture
def register_case_and_dependencies() -> Tuple[RegisterSaleUsecase, InMemoryProductRepository, MockMailer]:
    repo = InMemoryProductRepository()
    mailer = MockMailer()

    usecase = RegisterSaleUsecase(repo, mailer)
    
    return (usecase, repo, mailer)


def test_happy_path(register_case_and_dependencies) -> None:
    usecase, repo, mailer = register_case_and_dependencies
    product = ProductMother.create(stock=5)
    repo.save(product)

    usecase.run(product.name, 3)

    after_sale_product = repo.get_by_id(product.id)

    assert after_sale_product.stock == 2


def test_if_stock_left_zero_or_negative_then_mail_is_sent(register_case_and_dependencies) -> None:
    usecase, repo, mailer = register_case_and_dependencies
    product = ProductMother.create(stock=2)
    repo.save(product)

    usecase.run(product.name, 3)


    assert mailer.calls_count() == 2
