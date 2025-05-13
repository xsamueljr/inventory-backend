import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    yield
    os.unlink("test.db")
