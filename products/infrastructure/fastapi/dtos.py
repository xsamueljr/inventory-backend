from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, model_validator

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
    delivery_note_id: str
    amount: int = Field(gt=0)

    def map_to_dto(self) -> SaleDTO:
        return SaleDTO(
            self.product_id,
            self.amount,
            self.delivery_note_id
        )


class RegisterArrivalRequest(BaseModel):
    product_id: str
    amount: int = Field(gt=0)
    arriving_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_arrival_request(cls, model: "RegisterArrivalRequest"):
        if model.amount <= 0 and not model.arriving_date:
            raise ValueError("Sólo puedes poner 0 en la cantidad si proporcionas una fecha de llegada")
        
        return model

    def map_to_dto(self) -> ArrivalDTO:
        return ArrivalDTO(
            self.product_id,
            self.amount,
            self.arriving_date
        )
