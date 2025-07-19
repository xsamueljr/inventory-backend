from uuid import uuid4

from activity.domain.record_repository import RecordRepository
from activity.domain.record import Record, RecordKind
from auth.domain.logged_user_info import LoggedUserInfo
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository
from shared.domain.logger import Logger


class DeleteProductByIdUsecase:
    def __init__(self, logger: Logger, product_repository: ProductRepository, record_repository: RecordRepository) -> None:
        self.__logger = logger
        self.__repo = product_repository
        self.__record_repo = record_repository

    def run(self, user: LoggedUserInfo, id: str) -> None:
        product = self.__repo.get_by_id(id)
        if product is None:
            raise ProductNotFoundException(id)

        record = Record(
            id=str(uuid4()),
            kind=RecordKind.PRODUCT_DELETED,
            user_id=user.id,
            product_id=id,
            amount=product.stock,
        )

        self.__repo.delete(id)
        self.__record_repo.save(record)
        self.__logger.info(f"{user.name} ha borrado el {product.name} (ID {id})")
