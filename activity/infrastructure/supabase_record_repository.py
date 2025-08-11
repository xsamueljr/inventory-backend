from typing import Any, cast, Dict, List

import psycopg
from psycopg.rows import dict_row

from activity.domain.record import Record, RecordKind
from activity.domain.record_repository import RecordRepository
from shared.infrastructure.env import ENV


class SupabaseRecordRepository(RecordRepository):
    def __init__(self) -> None:
        self.conn = self.__connect()

    def save(self, record: Record) -> None:
        with self.__cursor() as cur:
            cur.execute(
                """
                INSERT INTO records (id, kind, user_id, product_id, amount, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    record.id,
                    record.kind.value,
                    record.user_id,
                    record.product_id,
                    record.amount,
                    record.created_at,
                ),
            )
        self.conn.commit()

    def get_by_user_id(self, id: str, limit: int, offset: int) -> List[Record]:
        with self.__cursor() as cur:
            cur.execute(
                """
                SELECT id, kind, user_id, product_id, amount, created_at
                FROM records
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (id, limit, offset),
            )
            rows = cur.fetchall()
            return [self.__to_record(cast(Dict[str, Any], r)) for r in rows]

    def get_all(self, limit: int, offset: int) -> List[Record]:
        with self.__cursor() as cur:
            cur.execute(
                """
                SELECT id, kind, user_id, product_id, amount, created_at
                FROM records
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            rows = cur.fetchall()
            return [self.__to_record(cast(Dict[str, Any], r)) for r in rows]

    def __to_record(self, row: Dict[str, Any]) -> Record:
        return Record(
            id=row["id"],
            kind=RecordKind(row["kind"]),
            user_id=row["user_id"],
            product_id=row["product_id"],
            amount=row["amount"],
            created_at=row["created_at"],
        )

    def __connect(self) -> psycopg.Connection:
        conninfo = ENV.SUPABASE_PG_CONN
        conn = psycopg.connect(conninfo, row_factory=dict_row)  # type: ignore
        conn.execute(f'SET search_path TO "{ENV.PG_SCHEMA}"')  # type: ignore
        return conn

    def __cursor(self) -> psycopg.Cursor:
        """Helper method that provides a cursor but handles disconnection first"""
        try:
            self.conn.execute("SELECT 1")  # ping
        except psycopg.OperationalError:
            self.conn = self.__connect()

        return self.conn.cursor()
