from dataclasses import dataclass

from emails.domain.emailer import Emailer
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository


@dataclass
class ArrivalDTO:
    id: str
    amount: int

    def __post_init__(self) -> None:
        if self.amount == 0:
            raise ValueError("¿Si no ha llegado nada qué haces?")
        
        if self.amount < 0:
            raise ValueError("¿Seguro que no querías hacer una venta?")


class RegisterArrivalUsecase:
    def __init__(
            self,
            repo: ProductRepository
    ) -> None:
        self.__repo = repo
    
    def run(self, input: ArrivalDTO) -> None:
        """Creates the new product or add stock to existing one"""
        product = self.__repo.get_by_id(input.id)
        if not product:
            raise ProductNotFoundException(input.id)
        
        product.stock += input.amount
        self.__repo.update(product)
