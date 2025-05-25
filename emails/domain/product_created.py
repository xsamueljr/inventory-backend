from emails.domain.email import Email
from products.domain.product import Product


class ProductCreatedEmail(Email):
    def __init__(self, user_name: str, product: Product) -> None:
        subject = "Se ha creado un producto"
        arrival_field = (
            f"Fecha de llegada: {product.arriving_date}"
            if product.arriving_date
            else ""
        )

        content = (
            f"{user_name} acaba de crear un producto con la siguiente info:",
            f"- Modelo: {product.name}",
            f"- Stock: {product.stock}",
            arrival_field,
        )

        super().__init__(subject, "\n".join(content))
