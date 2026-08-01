import psycopg
from psycopg.rows import dict_row

from locations.domain.location import Location
from locations.domain.location_repository import LocationRepository
from shared.infrastructure.env import ENV


class SupabaseLocationRepository(LocationRepository):
    def __init__(self):
        conninfo = ENV.SUPABASE_PG_CONN
        self.conn = psycopg.connect(conninfo, row_factory=dict_row)  # type: ignore
        self.conn.execute(f'SET search_path TO "{ENV.PG_SCHEMA}"')  # type: ignore

    def get_all(self) -> list[Location]:
        cur = self.conn.execute("SELECT id, name FROM locations")  # type: ignore
        return [self.__to_domain(row) for row in cur.fetchall()]  # type: ignore

    def __to_domain(self, row: dict) -> Location:
        return Location(
            id=row["id"],
            name=row["name"],
        )
