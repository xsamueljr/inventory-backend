from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from products.application.dtos.create_product import CreateProductDTO
from products.application.register_arrival import ArrivalDTO
from products.application.register_sell import SaleDTO


class CreateProductRequest(BaseModel):
    name: str
    stock: int
    arriving_date: Optional[date] = None

    def map_to_domain(self) -> CreateProductDTO:
        return CreateProductDTO(
            self.name,
            self.stock,
            self.arriving_date
        )


class RegisterSaleRequest(BaseModel):
    product_id: str
    amount: int = Field(gt=0)

    def map_to_dto(self) -> SaleDTO:
        return SaleDTO(
            self.product_id,
            self.amount
        )


class RegisterArrivalRequest(BaseModel):
    product_id: str
    amount: int = Field(gt=0)

    def map_to_dto(self) -> ArrivalDTO:
        return ArrivalDTO(
            self.product_id,
            self.amount
        )
