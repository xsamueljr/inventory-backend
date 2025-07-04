from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RecordKind(Enum):
    PRODUCT_CREATED = "product-created"
    PRODUCT_DELETED = "product-deleted"
    PRODUCT_SOLD = "product-sold"


@dataclass(slots=True, frozen=True)
class Record:
    id: str
    kind: RecordKind
    user_id: str
    product_id: str
    amount: int

    created_at: datetime = field(default_factory=datetime.now)
