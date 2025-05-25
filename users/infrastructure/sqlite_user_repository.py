import sqlite3
from typing import Any
from shared.infrastructure.sqlite_connection import get_connection
from shared.infrastructure.sqlite_error_codes import SQLiteErrorCodes
from users.domain.exceptions.user_already_exists import UserAlreadyExistsException
from users.domain.user import User
from users.domain.user_repository import UserRepository


class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str | None = None) -> None:
        if db_path:
            conn = get_connection(db_path)
        else:
            conn = get_connection()

        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            shop_name TEXT NOT NULL
        )
        """)

        self.__conn = conn

    def save(self, user: User) -> None:
        cur = self.__conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (id, username, password, shop_name) VALUES (?, ?, ?, ?)",
                (user.id, user.username, user.password, user.shop_name),
            )

            self.__conn.commit()
        except sqlite3.Error as e:
            if e.sqlite_errorcode == SQLiteErrorCodes.CONSTRAINT_UNIQUE:
                raise UserAlreadyExistsException(user.id)
            raise
        finally:
            cur.close()

    def get_by_id(self, id: str) -> User | None:
        return self.__get_one("id", id)

    def get_by_username(self, username: str) -> User | None:
        return self.__get_one("username", username)

    def __get_one(self, field: str, value: str) -> User | None:
        """Helper method for getting a user based on a single field

        Avoids duplication for getting by id and name"""

        cur = self.__conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE {field} = ?", (value,))
        result = cur.fetchone()
        cur.close()
        if result is None:
            return None
        return self.__map_to_domain(result)

    def __map_to_domain(self, row: Any) -> User:
        return User(id=row[0], username=row[1], password=row[2], shop_name=row[3])
