from emails.domain.email import Email
from products.domain.product import Product


class ProductCreatedEmail(Email):
    def __init__(self, from_: str, to: str, product: Product) -> None:
        subject = "Se ha creado un producto"

        content = f"""
            Se acaba de crear un producto con la siguiente info:
            - Modelo: {product.model}
            - Color: {product.color}
            - Stock: {product.stock}
        """.strip()

        
        super().__init__(from_, to, subject, content)