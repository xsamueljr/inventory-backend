from typing import Optional, Dict, Any, cast

import psycopg
from psycopg.rows import dict_row

from users.domain.user import User
from users.domain.user_repository import UserRepository
from shared.infrastructure.env import ENV


class SupabaseUserRepository(UserRepository):
    def __init__(self) -> None:
        self.conn = self.__connect()

    def save(self, user: User) -> None:
        with self.__cursor() as cur:
            cur.execute(
                """
                INSERT INTO app_users (id, username, password, shop_name)
                VALUES (%s, %s, %s, %s)
                """,
                (user.id, user.username, user.password, user.shop_name),
            )
        self.conn.commit()

    def get_by_id(self, id: str) -> Optional[User]:
        with self.__cursor() as cur:
            cur.execute(
                """
                SELECT id, username, password, shop_name FROM app_users WHERE id = %s
                """,
                (id,),
            )
            row = cur.fetchone()
            return self.__to_user(cast(Dict[str, Any], row)) if row else None

    def get_by_username(self, username: str) -> Optional[User]:
        with self.__cursor() as cur:
            cur.execute(
                """
                SELECT id, username, password, shop_name FROM app_users WHERE username = %s
                """,
                (username,),
            )
            row = cur.fetchone()
            return self.__to_user(cast(Dict[str, Any], row)) if row else None

    def __to_user(self, row: Dict[str, Any]) -> User:
        return User(
            id=str(row["id"]),
            username=row["username"],
            password=row["password"],
            shop_name=row["shop_name"],
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
