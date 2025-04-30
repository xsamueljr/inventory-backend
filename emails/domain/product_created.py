from emails.domain.email import Email
from products.domain.product import Product


class ProductCreatedEmail(Email):
    def __init__(self, product: Product) -> None:
        subject = "Se ha creado un producto"

        content = f"""
            Se acaba de crear un producto con la siguiente info:
            - Modelo: {product.name}
            - Color: {product.color}
            - Stock: {product.stock}
        """.strip()

        
        super().__init__(subject, content)