from dataclasses import dataclass

from emails.domain.email import Email
from emails.domain.emailer import Emailer
from emails.domain.stock_warning import StockWarningEmail
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository


@dataclass(frozen=True)
class SaleDTO:
    product_id: str
    amount: int

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("¿Una venta con cantidad negativa? ¿Seguro que esto no es una llegada?") # TODO: excepción personalizada


class RegisterSaleUsecase:

    def __init__(self, repo: ProductRepository, mailer: Emailer) -> None:
        self.__repo = repo
        self.__mailer = mailer
    
    def run(self, input: SaleDTO) -> None:
        product = self.__repo.get_by_id(input.product_id)
        if not product:
            raise ProductNotFoundException(input.product_id)
        
        new_stock = product.stock - input.amount
        product.stock = new_stock
        self.__repo.update(product)

        self.__mailer.send(Email(
            subject="Venta registrada",
            body=f"Se ha/n vendido {input.amount} unidad/es de {product.name}"
        )) # TODO: a lo mejor esto genera demasiados correos

        if new_stock <= 1:
            self.__mailer.send(StockWarningEmail(product))
