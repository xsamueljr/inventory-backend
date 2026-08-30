from typing import List

import psycopg
from psycopg.rows import dict_row

from locations.domain.location import Location
from locations.domain.location_repository import LocationRepository
from shared.infrastructure.database_credentials import DatabaseCredentials


class SupabaseLocationRepository(LocationRepository):
    def __init__(self, credentials: DatabaseCredentials) -> None:
        self.credentials = credentials
        conninfo = credentials.connection_string
        self.conn = psycopg.connect(conninfo, row_factory=dict_row)  # type: ignore
        self.conn.execute(f'SET search_path TO "{credentials.schema}"')  # type: ignore

    def get_all(self) -> List[Location]:
        cur = self.conn.execute("SELECT id, name FROM locations")  # type: ignore
        return [self.__to_domain(row) for row in cur.fetchall()]  # type: ignore

    def __to_domain(self, row: dict) -> Location:
        return Location(
            id=row["id"],
            name=row["name"],
        )
