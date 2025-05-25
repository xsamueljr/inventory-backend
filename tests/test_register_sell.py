from dataclasses import dataclass

import pytest

from products.application.register_sell import RegisterSaleUsecase
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.infrastructure.in_memory_product_repository import (
    InMemoryProductRepository,
)
from tests.mocks import MockMailer, MockLogger
from tests.mothers.product import ProductMother
from tests.mothers.sale import SaleDTOMother


@dataclass
class RegisterSaleSetup:
    usecase: RegisterSaleUsecase
    repo: InMemoryProductRepository
    mailer: MockMailer


@pytest.fixture
def sale_setup() -> RegisterSaleSetup:
    repo = InMemoryProductRepository()
    mailer = MockMailer()

    usecase = RegisterSaleUsecase(repo, mailer, MockLogger())

    return RegisterSaleSetup(usecase, repo, mailer)


def test_happy_path(sale_setup, mock_user) -> None:
    product = ProductMother.create(stock=5)
    sale_setup.repo.save(product)

    sale_setup.usecase.run(
        mock_user, SaleDTOMother.create(product_id=product.id, amount=3)
    )

    after_sale_product = sale_setup.repo.get_by_id(product.id)

    assert after_sale_product.stock == 2
    assert sale_setup.mailer.was_called_once()


def test_if_stock_left_zero_or_negative_then_another_mail_is_sent(
    sale_setup, mock_user
) -> None:
    product = ProductMother.create(stock=2)
    sale_setup.repo.save(product)

    sale_setup.usecase.run(
        mock_user, SaleDTOMother.create(product_id=product.id, amount=3)
    )

    assert sale_setup.mailer.calls_count() == 2


def test_cannot_register_sale_for_a_product_that_does_not_exist(
    sale_setup, mock_user
) -> None:
    with pytest.raises(ProductNotFoundException):
        sale_setup.usecase.run(
            mock_user, SaleDTOMother.create(product_id="irrelevant-id", amount=2)
        )


@pytest.mark.parametrize("amount", (0, -1, -5, -99))
def test_sale_with_zero_or_negative_amount_cannot_exist(amount) -> None:
    with pytest.raises(ValueError):
        SaleDTOMother.create(amount=amount)
