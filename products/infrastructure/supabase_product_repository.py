from typing import Optional, Dict, Any, cast, List

import psycopg
from psycopg.rows import dict_row

from shared.infrastructure.database_credentials import DatabaseCredentials
from products.domain.product import Product
from products.domain.product_repository import ProductRepository


class SupabaseProductRepository(ProductRepository):
    def __init__(self, credentials: DatabaseCredentials) -> None:
        self.credentials = credentials
        self.conn = self.__connect()

    def save(self, product: Product) -> None:
        with self.__cursor() as cur:
            # Intentar insertar solo si no existe
            cur.execute(
                """
                INSERT INTO products (id, name, stock, arriving_date, location_id)
                SELECT %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM products WHERE id = %s
                )
                """,
                (
                    product.id,
                    product.name,
                    product.stock,
                    product.arriving_date,
                    product.location_id,
                    product.id,
                ),
            )
        self.conn.commit()

    def update(self, product: Product) -> None:
        with self.__cursor() as cur:
            # Actualiza solo si ya existe
            cur.execute(
                """
                UPDATE products
                SET name = %s,
                    stock = %s,
                    arriving_date = %s,
                    location_id = %s,
                WHERE id = %s
                """,
                (
                    product.name,
                    product.stock,
                    product.arriving_date,
                    product.location_id,
                    product.id,
                ),
            )
        self.conn.commit()

    def get_by_id(self, id: str) -> Optional[Product]:
        with self.__cursor() as cur:
            cur.execute(
                "SELECT id, name, stock, arriving_date, location_id FROM products WHERE id = %s",
                (id,),
            )
            row = cur.fetchone()
            return self.__to_product(cast(Dict[str, Any], row)) if row else None

    def get_by_location(
        self, location_id: int, limit: int, offset: int
    ) -> List[Product]:
        with self.__cursor() as cur:
            cur.execute(
                "SELECT id, name, stock, arriving_date, location_id FROM products WHERE location_id = %s LIMIT %s OFFSET %s",
                (location_id, limit, offset),
            )
            rows = cur.fetchall()
            return [self.__to_product(cast(Dict[str, Any], r)) for r in rows]

    def get_by_name(self, name: str) -> Optional[Product]:
        with self.__cursor() as cur:
            cur.execute(
                "SELECT id, name, stock, arriving_date, location_id FROM products WHERE name = %s AND location_id IS NULL",
                (name,),
            )
            row = cur.fetchone()
            return self.__to_product(cast(Dict[str, Any], row)) if row else None

    def get_all(self, limit: int, offset: int) -> list[Product]:
        with self.__cursor() as cur:
            cur.execute(
                "SELECT id, name, stock, arriving_date, location_id FROM products WHERE location_id IS NULL LIMIT %s OFFSET %s",
                (limit, offset),
            )
            rows = cur.fetchall()
            return [self.__to_product(cast(Dict[str, Any], r)) for r in rows]

    def delete(self, id: str) -> None:
        with self.__cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s", (id,))
        self.conn.commit()

    def search_by_name(self, name: str) -> List[Product]:
        with self.__cursor() as cur:
            cur.execute(
                """
                SELECT id, name, stock, arriving_date, location_id
                FROM products
                WHERE name ILIKE %s
                """,
                (f"%{name.strip()}%",),
            )

            rows = cur.fetchall()
            return [self.__to_product(cast(Dict[str, Any], r)) for r in rows]

    def search_by_name_and_location(self, name: str, location_id: int) -> List[Product]:
        with self.__cursor() as cur:
            cur.execute(
                """
                SELECT id, name, stock, arriving_date, location_id
                FROM products
                WHERE name ILIKE %s AND location_id = %s
                """,
                (f"%{name.strip()}%", location_id),
            )
            rows = cur.fetchall()
            return [self.__to_product(cast(Dict[str, Any], r)) for r in rows]

    def __to_product(self, row: Dict[str, Any]) -> Product:
        return Product(
            id=row["id"],
            name=row["name"],
            stock=row["stock"],
            arriving_date=row["arriving_date"],
            location_id=row["location_id"],
        )

    def __connect(self) -> psycopg.Connection:
        conninfo = self.credentials.connection_string
        conn = psycopg.connect(conninfo, row_factory=dict_row)  # type: ignore
        conn.execute(f'SET search_path TO "{self.credentials.schema}"')  # type: ignore
        return conn

    def __cursor(self) -> psycopg.Cursor:
        """Helper method that provides a cursor but handles disconnection first"""
        try:
            self.conn.execute("SELECT 1")  # ping
        except psycopg.OperationalError:
            self.conn = self.__connect()

        return self.conn.cursor()
