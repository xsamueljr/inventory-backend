from dataclasses import dataclass
from typing import Tuple

import pytest

from products.application.register_sell import RegisterSaleUsecase, SaleDTO
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository
from tests.mocks import MockMailer
from tests.mothers.product import ProductMother


@dataclass
class RegisterSaleSetup:
    usecase: RegisterSaleUsecase
    repo: InMemoryProductRepository
    mailer: MockMailer


@pytest.fixture
def sell_setup() -> RegisterSaleSetup:
    repo = InMemoryProductRepository()
    mailer = MockMailer()

    usecase = RegisterSaleUsecase(repo, mailer)
    
    return RegisterSaleSetup(usecase, repo, mailer)


def test_happy_path(sell_setup) -> None:
    product = ProductMother.create(stock=5)
    sell_setup.repo.save(product)

    sell_setup.usecase.run(SaleDTO(product.id, 3))

    after_sale_product = sell_setup.repo.get_by_id(product.id)

    assert after_sale_product.stock == 2


def test_if_stock_left_zero_or_negative_then_mail_is_sent(sell_setup) -> None:
    product = ProductMother.create(stock=2)
    sell_setup.repo.save(product)

    sell_setup.usecase.run(SaleDTO(product.id, 3))

    assert sell_setup.mailer.calls_count() == 2
