from typing import Callable, List
import pytest
from emails.domain.email import Email
from emails.domain.emailer import Emailer
from products.domain.dtos.update_product import UpdateProductDTO
from products.domain.product import Product
from products.domain.product_repository import ProductRepository
from products.infrastructure.in_memory_product_repository import InMemoryProductRepository
from shared.domain.logger import Logger


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
        return self.__query(lambda product: product.name == name)
    
    def get_all(self, limit: int, offset: int) -> List[Product]:
        # purposefully not slicing the list
        return [product for product in self.__products]
    
    def update(self, product: Product) -> None:
        raise NotImplementedError(
            "Update method in mock product repository may not be needed right now (implement it otherwise)"
        )
    
    def delete(self, id: str) -> None:
        for i, product in enumerate(self.__products):
            if product.id == id:
                self.__products.pop(i)
                break
    
    def get_count(self) -> int:
        return len(self.__products)
    
    def search_by_name(self, name: str) -> List[Product]:
        return [product for product in self.__products if name.strip() in product.name.strip()]
    
    def __query(self, criteria: Callable[[Product], bool]) -> Product | None:
        return next(filter(criteria, self.__products), None)


class MockLogger(Logger):
    def info(self, message: str) -> None:
        ...
    
    def warning(self, message: str) -> None:
        ...
    
    def error(self, message: str) -> None:
        ...


@pytest.fixture
def mock_mailer() -> MockMailer:
    return MockMailer()


@pytest.fixture
def mock_product_repository() -> MockProductRepository:
    return MockProductRepository()
