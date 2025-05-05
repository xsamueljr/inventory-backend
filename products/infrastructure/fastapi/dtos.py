from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from products.application.dtos.create_product import CreateProductDTO


class CreateProductRequest(BaseModel):
    name: str
    color: str
    stock: int
    arriving_date: Optional[date]

    def map_to_domain(self) -> CreateProductDTO:
        return CreateProductDTO(
            self.name,
            self.color,
            self.stock,
            self.arriving_date
        )