import pytest


@pytest.fixture(scope="session", autouse=True)
def _session_fixture() -> None:
    pass
