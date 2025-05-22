from dataclasses import dataclass
from datetime import date
from typing import Optional

from auth.domain.logged_user_info import LoggedUserInfo
from emails.domain.emailer import Emailer
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository
from shared.domain.logger import Logger


@dataclass
class ArrivalDTO:
    id: str
    amount: int
    arriving_date: Optional[date] = None

    def __post_init__(self) -> None:
        if self.amount >= 0 and not self.arriving_date:
            raise ValueError("Sólo puedes poner 0 en la cantidad si proporcionas una fecha de llegada")


class RegisterArrivalUsecase:
    def __init__(
            self,
            logger: Logger,
            repo: ProductRepository
    ) -> None:
        self.__logger = logger
        self.__repo = repo
    
    def run(self, user: LoggedUserInfo, input: ArrivalDTO) -> None:
        product = self.__repo.get_by_id(input.id)
        if not product:
            raise ProductNotFoundException(input.id)
        
        product.stock += input.amount
        product.arriving_date = input.arriving_date
        self.__repo.update(product)
        self.__logger.info(
            f"{user.name} ha registrado que acaban de llegar "
            f"{input.amount} unidades de {product.name}"
        )
