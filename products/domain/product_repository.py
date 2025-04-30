from abc import ABC, abstractmethod
from typing import Optional

from products.domain.product import Product


class ProductRepository(ABC):
    
    @abstractmethod
    def save(self, product: Product) -> None: ...

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Product]: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Product]: ...
    
    @abstractmethod
    def update(self, product: Product) -> None: ...
