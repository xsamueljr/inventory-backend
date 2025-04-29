from dataclasses import dataclass
from datetime import date
from typing import Optional

from products.domain.product import Product


@dataclass
class CreateProductDTO:
    model: str
    color: str
    stock: int = 0
    arriving_date: Optional[date] = None
    
    def to_domain(self) -> Product:
        return Product(
            self.model,
            self.color,
            self.stock,
            self.arriving_date
        )