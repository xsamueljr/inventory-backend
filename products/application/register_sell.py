from dataclasses import dataclass

from auth.domain.logged_user_info import LoggedUserInfo
from emails.domain.email import Email
from emails.domain.emailer import Emailer
from emails.domain.stock_warning import StockWarningEmail
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository
from shared.domain.logger import Logger


@dataclass(frozen=True)
class SaleDTO:
    product_id: str
    amount: int
    delivery_note_id: str

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("¿Una venta con cantidad negativa? ¿Seguro que esto no es una llegada?") # TODO: excepción personalizada


class RegisterSaleUsecase:

    def __init__(self, repo: ProductRepository, mailer: Emailer, logger: Logger) -> None:
        self.__repo = repo
        self.__mailer = mailer
        self.__logger = logger
    
    def run(self, user: LoggedUserInfo, input: SaleDTO) -> None:
        product = self.__repo.get_by_id(input.product_id)
        if not product:
            raise ProductNotFoundException(input.product_id)
        
        new_stock = product.stock - input.amount
        product.stock = new_stock
        self.__repo.update(product)

        mail = Email(
            subject="Venta registrada",
            body=f"{user.name} ha vendido {input.amount} unidad/es de {product.name}\n"
            f"Albarán: {input.delivery_note_id}"
        )
        self.__mailer.send(mail)
        self.__logger.info(mail.body)

        if new_stock <= 1:
            self.__mailer.send(StockWarningEmail(product))
            self.__logger.info(f"Stock de {product.name} bajo. Correo enviado")