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
            repository: ProductRepository,
            mailer: Emailer
    ) -> None:
        self.__logger = logger
        self.__repository = repository
        self.__mailer = mailer
    
    def run(self, user: LoggedUserInfo, input: CreateProductDTO) -> str:
        product = input.to_domain()
        self.__repository.save(product)

        mail = ProductCreatedEmail(user.name, product)
        self.__mailer.send(mail)
        self.__logger.info(mail.body)

        return product.id
