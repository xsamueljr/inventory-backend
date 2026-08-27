from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import uuid4


@dataclass
class Product:
    name: str
    stock: int
    arriving_date: Optional[date] = None

    id: str = field(default_factory=lambda: str(uuid4()))
    location_id: int | None = None

    def has_low_stock(self) -> bool:
        return self.stock <= 1

    def is_global(self) -> bool:
        return self.location_id is None

    def is_local(self) -> bool:
        return self.location_id is not None
