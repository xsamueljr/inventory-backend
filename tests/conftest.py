import os
import pytest

from auth.domain.logged_user_info import LoggedUserInfo


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
    return LoggedUserInfo("irrelevant-id", "irrelevant-name")
