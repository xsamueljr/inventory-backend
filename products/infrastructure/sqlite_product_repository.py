import sqlite3
from typing import Any, List

from products.domain.exceptions.product_already_exists import ProductAlreadyExistsException
from products.domain.product import Product
from products.domain.product_repository import ProductRepository
from shared.infrastructure.sqlite_connection import get_connection
from shared.infrastructure.sqlite_error_codes import SQLiteErrorCodes


class SQLiteProductRepository(ProductRepository):

    def __init__(self, db_path: str | None = None) -> None:
        if db_path:
            conn = get_connection(db_path)
        else:
            conn = get_connection()

        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL,
            arriving_date TEXT
        )
        """)

        self.__conn = conn
    
    def save(self, product: Product) -> None:
        cur = self.__conn.cursor()
        try:
            cur.execute("INSERT INTO products (id, name, stock, arriving_date) VALUES (?, ?, ?, ?)", (
                product.id, product.name, product.stock, product.arriving_date
            ))

            self.__conn.commit()
        except sqlite3.Error as e:
            if e.sqlite_errorcode == SQLiteErrorCodes.CONSTRAINT_UNIQUE:
                raise ProductAlreadyExistsException(id=product.id)
            raise
        finally:
            cur.close()

    def get_by_id(self, id: str) -> Product | None:
        return self.__get_one("id", id)
    
    def get_by_name(self, name: str) -> Product | None:
        return self.__get_one("name", name)
    
    def get_all(self) -> List[Product]:
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM products")
        result = cur.fetchall()
        cur.close()
        return [self.__map_to_domain(row) for row in result]
    
    def update(self, product: Product) -> None:
        cur = self.__conn.cursor()
        cur.execute("UPDATE products SET name=?, stock=?, arriving_date=? WHERE id=?", (
            product.name, product.stock, product.arriving_date, product.id
        ))
        self.__conn.commit()
        cur.close()

    def __get_one(self, field: str, value: str) -> Product | None:
        """Helper method for getting a product based on a single field
        
        Avoids duplication for getting by id and name"""

        cur = self.__conn.cursor()
        cur.execute(f"SELECT * FROM products WHERE {field} = ?", (value,))
        result = cur.fetchone()
        cur.close()
        if result is None:
            return None
        return self.__map_to_domain(result)

    def __map_to_domain(self, row: Any) -> Product:
        return Product(
            id=row[0],
            name=row[1],
            stock=row[2],
            arriving_date=row[3]
        )