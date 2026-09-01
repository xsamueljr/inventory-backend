from datetime import date
from products.domain.product import Product
from products.infrastructure.supabase_product_repository import (
    SupabaseProductRepository,
)
from shared.infrastructure.database_credentials import DatabaseCredentials


def test_supabase_product_repository_save_and_get_by_id(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseProductRepository(postgres_credentials)

    product = Product(
        id="prod-1",
        name="Mesa de madera",
        stock=10,
        arriving_date=date(2026, 9, 15),
        location_id=1,
    )

    repo.save(product)

    fetched = repo.get_by_id("prod-1")
    assert fetched is not None
    assert fetched.id == "prod-1"
    assert fetched.name == "Mesa de madera"
    assert fetched.stock == 10
    assert fetched.arriving_date == date(2026, 9, 15)
    assert fetched.location_id == 1


def test_supabase_product_repository_update(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseProductRepository(postgres_credentials)

    product = Product(
        id="prod-2",
        name="Silla de oficina",
        stock=5,
        location_id=1,
    )
    repo.save(product)

    product.name = "Silla ergonómica"
    product.stock = 8
    product.location_id = 2
    repo.update(product)

    fetched = repo.get_by_id("prod-2")
    assert fetched is not None
    assert fetched.name == "Silla ergonómica"
    assert fetched.stock == 8
    assert fetched.location_id == 2


def test_supabase_product_repository_get_by_location(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseProductRepository(postgres_credentials)

    p1 = Product(id="p1", name="Prod A", stock=1, location_id=10)
    p2 = Product(id="p2", name="Prod B", stock=2, location_id=10)
    p3 = Product(id="p3", name="Prod C", stock=3, location_id=20)

    repo.save(p1)
    repo.save(p2)
    repo.save(p3)

    loc10_prods = repo.get_by_location(10, limit=10, offset=0)
    assert len(loc10_prods) == 2
    ids = [p.id for p in loc10_prods]
    assert "p1" in ids
    assert "p2" in ids


def test_supabase_product_repository_global_products(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseProductRepository(postgres_credentials)

    global_p = Product(id="gp1", name="Global Item", stock=100, location_id=None)
    local_p = Product(id="lp1", name="Global Item", stock=50, location_id=5)

    repo.save(global_p)
    repo.save(local_p)

    fetched_by_name = repo.get_by_name("Global Item")
    assert fetched_by_name is not None
    assert fetched_by_name.id == "gp1"

    all_globals = repo.get_all(limit=10, offset=0)
    assert len(all_globals) == 1
    assert all_globals[0].id == "gp1"


def test_supabase_product_repository_delete(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseProductRepository(postgres_credentials)

    product = Product(id="to-delete", name="Temp Item", stock=1)
    repo.save(product)

    assert repo.get_by_id("to-delete") is not None

    repo.delete("to-delete")
    assert repo.get_by_id("to-delete") is None


def test_supabase_product_repository_search(
    postgres_credentials: DatabaseCredentials,
):
    repo = SupabaseProductRepository(postgres_credentials)

    p1 = Product(id="s1", name="Super Armario", stock=2, location_id=None)
    p2 = Product(id="s2", name="Armario pequeño", stock=3, location_id=3)

    repo.save(p1)
    repo.save(p2)

    global_search = repo.search_by_name("armario")
    assert len(global_search) == 1
    assert global_search[0].id == "s1"

    location_search = repo.search_by_name_and_location("armario", 3)
    assert len(location_search) == 1
    assert location_search[0].id == "s2"
