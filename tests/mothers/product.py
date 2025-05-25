from datetime import date
from faker import Faker
from products.domain.product import Product


class ProductMother:
    @staticmethod
    def create(
        *,
        model: str | None = None,
        stock: int | None = None,
        arriving_date: date | None = None,
        id: str | None = None,
    ) -> Product:
        faker = Faker()

        return Product(
            model or faker.name(),
            stock or faker.random_number(),
            arriving_date,
            id or faker.uuid4(),
        )
