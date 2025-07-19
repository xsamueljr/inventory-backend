from dataclasses import dataclass
from datetime import datetime

from activity.domain.record import RecordKind


@dataclass(frozen=True, slots=True)
class PublicRecordInfo:
    kind: RecordKind
    amount: int
    product_name: str
    user_name: str
    created_at: datetime
