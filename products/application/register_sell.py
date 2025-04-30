from emails.domain.email import Email
from emails.domain.emailer import Emailer
from emails.domain.stock_warning import StockWarningEmail
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository


class RegisterSaleUsecase:

    def __init__(self, repo: ProductRepository, mailer: Emailer) -> None:
        self.__repo = repo
        self.__mailer = mailer
    
    def run(self, name: str, amount: int) -> None:
        if amount <= 0:
            raise ValueError("¿Una venta con cantidad negativa? ¿Seguro que esto no es una llegada?") # TODO: excepción personalizada
        
        product = self.__repo.get_by_name(name)
        if not product:
            raise ProductNotFoundException()
        
        new_stock = product.stock - amount
        product.stock = new_stock
        self.__repo.update(product)

        self.__mailer.send(Email(
            subject="Venta registrada",
            body=f"Se ha/n vendido {amount} unidad/es de {name}"
        )) # TODO: a lo mejor esto genera demasiados correos

        if new_stock <= 0:
            self.__mailer.send(StockWarningEmail(product))
