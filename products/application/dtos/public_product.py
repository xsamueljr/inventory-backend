from typing import Optional
from dataclasses import dataclass
from datetime import date

from products.domain.product import Product


@dataclass(frozen=True)
class PublicProductInfo:
    id: str
    name: str
    stock: int
    arriving_date: Optional[date]

    @classmethod
    def from_domain(cls, product: Product) -> "PublicProductInfo":
        return cls(product.id, product.name, product.stock, product.arriving_date)
