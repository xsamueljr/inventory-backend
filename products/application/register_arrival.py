from dataclasses import dataclass

from emails.domain.emailer import Emailer
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository


@dataclass
class ArrivalDTO:
    name: str
    amount: int

    def __post_init__(self) -> None:
        if self.amount == 0:
            raise ValueError("¿Si no ha llegado nada qué haces?")
        
        if self.amount < 0:
            raise ValueError("¿Seguro que no querías hacer una venta?")


class RegisterArrivalUsecase:
    def __init__(
            self,
            repo: ProductRepository,
            mailer: Emailer
    ) -> None:
        self.__repo = repo
        self.__mailer = mailer
    
    def run(self, input: ArrivalDTO) -> None:
        """Creates the new product or add stock to existing one"""
        product = self.__repo.get_by_name(input.name)
        if not product:
            raise ProductNotFoundException()
        
        product.stock += input.amount
        self.__repo.update(product)
