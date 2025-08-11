from typing import Any, List
from datetime import datetime

from activity.domain.record import Record, RecordKind
from activity.domain.record_repository import RecordRepository
from shared.infrastructure.sqlite_connection import get_connection


class SQLiteRecordRepository(RecordRepository):
    def __init__(self, db_path: str | None = None) -> None:
        conn = get_connection(db_path) if db_path else get_connection()

        conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            user_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            amount INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            delivery_note_id TEXT
        )
        """)
        conn.commit()

        self.__conn = conn

    def save(self, record: Record) -> None:
        cur = self.__conn.cursor()
        cur.execute(
            "INSERT INTO records (id, kind, user_id, product_id, amount, created_at, delivery_note_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                record.id,
                record.kind.value,
                record.user_id,
                record.product_id,
                record.amount,
                record.created_at.isoformat(),
                record.delivery_note_id
            ),
        )

        self.__conn.commit()
        cur.close()

    def get_all(self, limit: int, offset: int) -> List[Record]:
        cur = self.__conn.cursor()
        cur.execute(
            "SELECT * FROM records ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        result = cur.fetchall()
        cur.close()
        return [self.__map_to_domain(row) for row in result]

    def get_by_user_id(self, id: str, limit: int, offset: int) -> List[Record]:
        cur = self.__conn.cursor()
        cur.execute(
            "SELECT * FROM records WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (id, limit, offset),
        )
        result = cur.fetchall()
        cur.close()
        return [self.__map_to_domain(row) for row in result]

    def __map_to_domain(self, row: Any) -> Record:
        return Record(
            id=row[0],
            kind=RecordKind(row[1]),
            user_id=row[2],
            product_id=row[3],
            amount=row[4],
            created_at=datetime.fromisoformat(row[5]),
            delivery_note_id=row[6]
        )
