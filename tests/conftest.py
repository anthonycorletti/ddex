import socket
from typing import Any, Generator

import pytest

_original_connect = socket.socket.connect


def patched_connect(*args: Any, **kwargs: Any) -> None:
    raise Exception("No internet connection allowed for tests.")


@pytest.fixture()
def enable_network() -> Generator:
    socket.socket.connect = _original_connect  # type: ignore
    yield
    socket.socket.connect = patched_connect  # type: ignore


@pytest.fixture()
def disable_network() -> Generator:
    # TODO: add to tests to avoid network connection so that tests run faster
    socket.socket.connect = patched_connect  # type: ignore
    yield
    socket.socket.connect = _original_connect  # type: ignore
