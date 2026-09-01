import psycopg
from locations.infrastructure.supabase_location_repository import (
    SupabaseLocationRepository,
)
from shared.infrastructure.database_credentials import DatabaseCredentials


def test_supabase_location_repository_get_all(
    postgres_credentials: DatabaseCredentials,
):
    # Insert initial locations manually
    with psycopg.connect(postgres_credentials.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO locations (id, name) VALUES (1, 'Central Warehouse'), (2, 'North Store');"
            )
        conn.commit()

    repo = SupabaseLocationRepository(postgres_credentials)
    locations = repo.get_all()

    assert len(locations) == 2
    names = [loc.name for loc in locations]
    assert "Central Warehouse" in names
    assert "North Store" in names
