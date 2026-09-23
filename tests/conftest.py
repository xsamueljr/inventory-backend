import os
import pytest
import psycopg

try:
    from testcontainers.community.postgres import PostgresContainer
except ImportError:
    from testcontainers.postgres import PostgresContainer

from auth.domain.logged_user_info import LoggedUserInfo
from shared.infrastructure.database_credentials import DatabaseCredentials


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    yield
    try:
        os.unlink("test.db")
    except FileNotFoundError:
        # no need to clean db then
        pass


@pytest.fixture
def mock_user() -> LoggedUserInfo:
    return LoggedUserInfo("irrelevant-id", "irrelevant-name", location_id=1)


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        conn_url = postgres.get_connection_url()
        if "://" in conn_url and "+" in conn_url.split("://")[0]:
            conn_url = "postgresql://" + conn_url.split("://", 1)[1]

        with psycopg.connect(conn_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS app_users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    shop_name TEXT NOT NULL,
                    location_id INTEGER NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user'
                );

                CREATE TABLE IF NOT EXISTS locations (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    stock INTEGER NOT NULL,
                    arriving_date DATE,
                    location_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY,
                    kind TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL,
                    delivery_note_id TEXT
                );
                """)
            conn.commit()

        yield conn_url


@pytest.fixture
def postgres_credentials(postgres_container: str) -> DatabaseCredentials:
    credentials = DatabaseCredentials(
        connection_string=postgres_container,
        schema="public",
    )
    with psycopg.connect(credentials.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE app_users, locations, products, records CASCADE;")
        conn.commit()

    return credentials
