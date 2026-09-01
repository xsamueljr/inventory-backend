from datetime import datetime, timezone
from activity.domain.record import Record, RecordKind
from activity.infrastructure.supabase_record_repository import SupabaseRecordRepository
from shared.infrastructure.database_credentials import DatabaseCredentials


def test_supabase_record_repository_save_and_get(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseRecordRepository(postgres_credentials)

    rec1 = Record(
        id="rec-1",
        kind=RecordKind.PRODUCT_CREATED,
        user_id="user-100",
        product_id="prod-100",
        amount=5,
        created_at=datetime.now(timezone.utc),
    )

    rec2 = Record(
        id="rec-2",
        kind=RecordKind.PRODUCT_SOLD,
        user_id="user-100",
        product_id="prod-100",
        amount=2,
        delivery_note_id="ALB-123",
        created_at=datetime.now(timezone.utc),
    )

    rec3 = Record(
        id="rec-3",
        kind=RecordKind.PRODUCT_DELETED,
        user_id="user-200",
        product_id="prod-200",
        amount=1,
        created_at=datetime.now(timezone.utc),
    )

    repo.save(rec1)
    repo.save(rec2)
    repo.save(rec3)

    user100_records = repo.get_by_user_id("user-100", limit=10, offset=0)
    assert len(user100_records) == 2
    rec_ids = [r.id for r in user100_records]
    assert "rec-1" in rec_ids
    assert "rec-2" in rec_ids

    sold_rec = next(r for r in user100_records if r.id == "rec-2")
    assert sold_rec.delivery_note_id == "ALB-123"
    assert sold_rec.kind == RecordKind.PRODUCT_SOLD

    all_records = repo.get_all(limit=10, offset=0)
    assert len(all_records) == 3
