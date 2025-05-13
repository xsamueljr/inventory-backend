from emails.domain.email import Email
from products.domain.product import Product


class ProductCreatedEmail(Email):
    def __init__(self, product: Product) -> None:
        subject = "Se ha creado un producto"

        content = (
            "Se acaba de crear un producto con la siguiente info:"
            f"- Modelo: {product.name}",
            f"- Stock: {product.stock}"
        )
        
        super().__init__(subject, "\n".join(content))