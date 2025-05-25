from emails.domain.email import Email
from products.domain.product import Product


class StockWarningEmail(Email):
    def __init__(self, product: Product) -> None:
        subject = "Hay un producto con stock negativo"
        body = f'El producto "{product.name}" (ID: {product.id}) tiene un stock de {product.stock}'

        super().__init__(subject, body)
