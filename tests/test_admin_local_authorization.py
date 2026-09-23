import pytest
from fastapi import HTTPException

from auth.domain.logged_user_info import LoggedUserInfo
from products.application.search_by_name import SearchProductsByNameUsecase
from products.domain.product import Product
from products.infrastructure.fastapi.helpers import resolve_local_location_id
from tests.mocks import MockProductRepository
from users.domain.user import User, UserRole


def test_logged_user_info_from_domain_sets_admin_flag():
    user = User(
        id="u-1",
        username="admin-user",
        password="secret",
        shop_name="Shop",
        location_id=7,
        role=UserRole.ADMIN,
    )

    info = LoggedUserInfo.from_domain(user)

    assert info.is_admin is True
    assert info.location_id == 7


def test_regular_user_cannot_access_other_location():
    user = LoggedUserInfo(id="u-1", name="regular", location_id=3, is_admin=False)

    with pytest.raises(HTTPException) as exc:
        resolve_local_location_id(user, 5)

    assert exc.value.status_code == 403


def test_admin_uses_requested_location_for_local_queries():
    user = LoggedUserInfo(id="u-1", name="admin", location_id=1, is_admin=True)

    assert resolve_local_location_id(user, 9) == 9
    assert resolve_local_location_id(user, None) == 1


def test_local_search_uses_location_filter():
    repo = MockProductRepository()
    repo.save(Product(id="g1", name="Sofá global", stock=5, location_id=None))
    repo.save(Product(id="l1", name="Sofá local", stock=5, location_id=3))
    repo.save(Product(id="l2", name="Mesa local", stock=2, location_id=3))

    usecase = SearchProductsByNameUsecase(repo)

    results = usecase.run("sofá", 3)

    assert [p.id for p in results] == ["l1"]


def test_regular_user_create_local_ignores_foreign_location():
    user = LoggedUserInfo(id="u-1", name="regular", location_id=3, is_admin=False)

    assert resolve_local_location_id(user, 10, mode="create") == 3
