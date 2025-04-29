from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class UpdateProductDTO:
    model: Optional[str] = None
    color: Optional[str] = None
    stock: Optional[int] = None
    arriving_date: Optional[date] = None
