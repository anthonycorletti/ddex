import os

from ddex.main import foo


def test_timezone() -> None:
    assert foo() == "foo"
    assert os.environ["TZ"] == "UTC"
