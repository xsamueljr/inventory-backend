from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo
from enum import Enum

MADRID_TZ = ZoneInfo("Europe/Madrid")

class RecordKind(Enum):
    PRODUCT_CREATED = "product-created"
    PRODUCT_ARRIVED = "product-arrived"
    PRODUCT_DELETED = "product-deleted"
    PRODUCT_SOLD = "product-sold"


@dataclass(slots=True, frozen=True)
class Record:
    id: str
    kind: RecordKind
    user_id: str
    product_id: str
    amount: int

    created_at: datetime = field(default_factory=lambda: datetime.now(MADRID_TZ))
