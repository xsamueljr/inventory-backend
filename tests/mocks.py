from typing import Callable, List
import pytest
from emails.domain.email import Email
from emails.domain.emailer import Emailer
from products.domain.dtos.update_product import UpdateProductDTO
from products.domain.product import Product
from products.domain.product_repository import ProductRepository
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository


class MockMailer(Emailer):

    def __init__(self) -> None:
        self.__calls: List[Email] = []
    
    def send(self, email: Email) -> None:
        self.__calls.append(email)
    
    def was_called_once(self) -> bool:
        return len(self.__calls) == 1

    def calls_count(self) -> int:
        return len(self.__calls)


class MockProductRepository(ProductRepository):
    
    def __init__(self) -> None:
        self.__products: List[Product] = []
    
    def save(self, product: Product) -> None:
        return self.__products.append(product)
    
    def get_by_id(self, id: str) -> Product | None:
        return self.__query(lambda product: product.id == id)
    
    def get_by_name(self, name: str) -> Product | None:
        return self.__query(lambda product: product.id == name)
    
    def get_all(self) -> List[Product]:
        return [product for product in self.__products]
    
    def update(self, product: Product) -> None:
        raise NotImplementedError(
            "Update method in mock product repository may not be needed right now (implement it otherwise)"
        )
    
    def __query(self, criteria: Callable[[Product], bool]) -> Product | None:
        return list(filter(criteria, self.__products))[0]


@pytest.fixture
def mock_mailer() -> MockMailer:
    return MockMailer()


@pytest.fixture
def mock_product_repository() -> MockProductRepository:
    return MockProductRepository()
