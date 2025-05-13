from functools import lru_cache
import sqlite3


@lru_cache
def get_connection(db_path: str = "db.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    return conn
