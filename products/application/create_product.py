from uuid import uuid4
from activity.domain.record import Record, RecordKind
from activity.domain.record_repository import RecordRepository
from auth.domain.logged_user_info import LoggedUserInfo
from shared.domain.logger import Logger
from emails.domain.emailer import Emailer
from emails.domain.product_created import ProductCreatedEmail
from products.application.dtos.create_product import CreateProductDTO
from products.domain.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(
        self,
        logger: Logger,
        product_repo: ProductRepository,
        record_repo: RecordRepository,
        mailer: Emailer,
    ) -> None:
        self.__logger = logger
        self.__product_repo = product_repo
        self.__record_repo = record_repo
        self.__mailer = mailer

    def run(self, user: LoggedUserInfo, input: CreateProductDTO) -> str:
        product = input.to_domain()
        self.__product_repo.save(product)

        record = Record(
            id=str(uuid4()),
            kind=RecordKind.PRODUCT_CREATED,
            user_id=user.id,
            product_id=product.id,
            amount=input.stock,
        )
        self.__record_repo.save(record)

        mail = ProductCreatedEmail(user.name, product)
        self.__mailer.send(mail)
        self.__logger.info(mail.body)

        return product.id
