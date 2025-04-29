from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import uuid4


@dataclass
class Product:
    model: str
    color: str
    stock: int
    arriving_date: Optional[date] = None

    id: str = field(default_factory=lambda: str(uuid4()))
