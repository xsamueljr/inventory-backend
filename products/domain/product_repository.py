from abc import ABC, abstractmethod
from typing import List, Optional

from products.domain.product import Product


class ProductRepository(ABC):
    
    @abstractmethod
    def save(self, product: Product) -> None: ...

    @abstractmethod
    def get_all(self, limit: int, offset: int) -> List[Product]: ...
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Product]: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Product]: ...
    
    @abstractmethod
    def update(self, product: Product) -> None: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...

    @abstractmethod
    def search_by_name(self, name: str) -> List[Product]: ...
