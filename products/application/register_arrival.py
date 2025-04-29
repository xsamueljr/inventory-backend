from dataclasses import dataclass

from emails.domain.email_sender import EmailSender
from products.application.dtos.create_product import CreateProductDTO
from products.domain.dtos.update_product import UpdateProductDTO
from products.domain.product_repository import ProductRepository


@dataclass
class ArrivalDTO:
    model: str
    amount: int

    def __post_init__(self) -> None:
        if self.amount == 0:
            raise ValueError("¿Si no han llegado nada qué haces?")
        
        if self.amount < 0:
            raise ValueError("¿Seguro que no querías hacer una venta?")


class RegisterArrivalUsecase:
    def __init__(
            self,
            repo: ProductRepository,
            mailer: EmailSender
    ) -> None:
        self.__repo = repo
        self.__mailer = mailer
    
    def run(self, input: CreateProductDTO) -> str:
        """Creates the new product or add stock to existing one"""

        existing_product = self.__repo.get_by_name(input.model)
        if not existing_product:
            product = input.to_domain()
            self.__repo.save(input.to_domain())
            return product.id
        else:
            new_stock = existing_product.stock + input.stock
            self.__repo.update(existing_product.id, UpdateProductDTO(stock=new_stock))
            return existing_product.id
