from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import uuid4

from activity.domain.record import Record, RecordKind
from activity.domain.record_repository import RecordRepository
from auth.domain.logged_user_info import LoggedUserInfo
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository
from shared.domain.logger import Logger


@dataclass
class ArrivalDTO:
    id: str
    amount: int
    arriving_date: Optional[date] = None

    def __post_init__(self) -> None:
        if self.amount <= 0 and not self.arriving_date:
            raise ValueError(
                "Sólo puedes poner 0 en la cantidad si proporcionas una fecha de llegada"
            )


class RegisterArrivalUsecase:
    def __init__(
        self,
        logger: Logger,
        product_repo: ProductRepository,
        record_repo: RecordRepository
    ) -> None:
        self.__logger = logger
        self.__product_repo = product_repo
        self.__record_repo = record_repo

    def run(self, user: LoggedUserInfo, input: ArrivalDTO) -> None:
        product = self.__product_repo.get_by_id(input.id)
        if not product:
            raise ProductNotFoundException(input.id)

        product.stock += input.amount
        product.arriving_date = input.arriving_date
        self.__product_repo.update(product)

        record = Record(
            id=str(uuid4()),
            kind=RecordKind.PRODUCT_ARRIVED,
            user_id=user.id,
            product_id=product.id,
            amount=input.amount
        )
        self.__record_repo.save(record)

        self.__logger.info(
            f"{user.name} ha registrado que acaban de llegar "
            f"{input.amount} unidades de {product.name}"
        )
