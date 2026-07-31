from dataclasses import dataclass
from datetime import datetime

from activity.domain.record import Record, RecordKind


@dataclass(frozen=True, slots=True)
class PublicRecordInfo:
    kind: RecordKind
    amount: int
    product_name: str
    user_name: str
    created_at: datetime
    delivery_note_id: str | None = None

    @classmethod
    def from_domain(cls, record: Record, product_name: str, user_name: str) -> "PublicRecordInfo":
        return cls(
            kind=record.kind,
            amount=record.amount,
            product_name=product_name,
            user_name=user_name,
            created_at=record.created_at,
            delivery_note_id=record.delivery_note_id
        )
