import os
import pytest

from auth.domain.logged_user_info import LoggedUserInfo


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    yield
    os.unlink("test.db")


@pytest.fixture
def mock_user() -> LoggedUserInfo:
    return LoggedUserInfo(
        "irrelevant-id",
        "irrelevant-name"
    )
