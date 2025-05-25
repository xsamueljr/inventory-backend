from products.application.register_sell import SaleDTO


class SaleDTOMother:
    @staticmethod
    def create(
        *,
        product_id: str = "irrelevant-id",
        amount: int = 2,
        delivery_note_id: str = "irrelevant-id",
    ) -> SaleDTO:
        return SaleDTO(
            product_id=product_id,
            amount=amount,
            delivery_note_id=delivery_note_id,
        )
