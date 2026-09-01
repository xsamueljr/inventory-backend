from shared.infrastructure.database_credentials import DatabaseCredentials
from users.domain.user import User
from users.infrastructure.supabase_user_repository import SupabaseUserRepository


def test_supabase_user_repository_save_and_get_by_id(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseUserRepository(postgres_credentials)

    user = User(
        id="user-1",
        username="john_doe",
        password="secret_password",
        shop_name="Doe Shop",
        location_id=1,
    )

    repo.save(user)

    fetched = repo.get_by_id("user-1")
    assert fetched is not None
    assert fetched.id == "user-1"
    assert fetched.username == "john_doe"
    assert fetched.password == "secret_password"
    assert fetched.shop_name == "Doe Shop"
    assert fetched.location_id == 1


def test_supabase_user_repository_get_by_username(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseUserRepository(postgres_credentials)

    user = User(
        id="user-2",
        username="jane_doe",
        password="password123",
        shop_name="Jane Shop",
        location_id=2,
    )

    repo.save(user)

    fetched = repo.get_by_username("jane_doe")
    assert fetched is not None
    assert fetched.id == "user-2"
    assert fetched.username == "jane_doe"


def test_supabase_user_repository_get_non_existent(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseUserRepository(postgres_credentials)

    assert repo.get_by_id("non-existent") is None
    assert repo.get_by_username("non-existent") is None
