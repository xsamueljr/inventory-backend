import sqlite3
from typing import Any
from shared.infrastructure.sqlite_connection import get_connection
from shared.infrastructure.sqlite_error_codes import SQLiteErrorCodes
from users.domain.exceptions.user_already_exists import UserAlreadyExistsException
from users.domain.user import User, UserRole
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
            shop_name TEXT NOT NULL,
            location_id INTEGER NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
        """)

        columns = conn.execute("PRAGMA table_info(users)").fetchall()
        if not any(column[1] == "role" for column in columns):
            conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")

        self.__conn = conn

    def save(self, user: User) -> None:
        cur = self.__conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (id, username, password, shop_name, location_id, role) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    user.id,
                    user.username,
                    user.password,
                    user.shop_name,
                    user.location_id,
                    user.role.value,
                ),
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
        role_value = row[5] if len(row) > 5 and row[5] is not None else "user"
        return User(
            id=row[0],
            username=row[1],
            password=row[2],
            shop_name=row[3],
            location_id=row[4],
            role=UserRole(role_value),
        )
