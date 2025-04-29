from dataclasses import dataclass
from emails.application.dtos.email_config import EmailConfig
from emails.domain.email_sender import EmailSender
from emails.domain.product_created import ProductCreatedEmail
from products.application.dtos.create_product import CreateProductDTO
from products.domain.product_repository import ProductRepository





class CreateProductUseCase:
    def __init__(self, repository: ProductRepository, mailer: EmailSender, config: EmailConfig) -> None:
        self.__repository = repository
        self.__mailer = mailer
        self.__config = config
    
    def run(self, input: CreateProductDTO) -> str:
        product = input.to_domain()
        self.__repository.save(product)

        mail = ProductCreatedEmail(from_=self.__config.gmail_address, to=self.__config.boss_email, product=product)
        self.__mailer.send(mail)

        return product.id
