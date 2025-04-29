from emails.domain.email import Email
from emails.domain.email_sender import EmailSender
from products.domain.dtos.update_product import UpdateProductDTO
from products.domain.exceptions.product_not_found import ProductNotFoundException
from products.domain.product_repository import ProductRepository


class RegisterSaleUsecase:

    def __init__(self, repo: ProductRepository, mailer: EmailSender) -> None:
        self.__repo = repo
        self.__mailer = mailer
    
    def run(self, model: str, amount: int) -> None:
        if amount <= 0:
            raise ValueError("¿Una venta con cantidad negativa? ¿Seguro que esto no es una llegada?")
        
        product = self.__repo.get_by_name(model)
        if not product:
            raise ProductNotFoundException()
        
        new_stock = product.stock - amount
        if new_stock < 0:
            raise ValueError("No puedes dejar el stock en negativo") # preguntar si sí

        update = UpdateProductDTO(stock=new_stock)
        self.__repo.update(product.id, update)

        self.__mailer.send(Email(
            subject="Venta registrada",
            body=f"Se ha/n vendido {amount} unidad/es de {model}"
        ))