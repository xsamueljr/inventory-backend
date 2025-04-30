from emails.domain.emailer import Emailer
from emails.domain.product_created import ProductCreatedEmail
from products.application.dtos.create_product import CreateProductDTO
from products.domain.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(self, repository: ProductRepository, mailer: Emailer) -> None:
        self.__repository = repository
        self.__mailer = mailer
    
    def run(self, input: CreateProductDTO) -> str:
        product = input.to_domain()
        self.__repository.save(product)

        mail = ProductCreatedEmail(product)
        self.__mailer.send(mail)

        return product.id
