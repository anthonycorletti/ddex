import pytest

from ddex import load_ddex_xsd_schema
from ddex.exc import DDEXException


def test_load_ddex_xsd_to_valid_object() -> None:
    ddex_schema = load_ddex_xsd_schema(
        path="tests/assets/schemas/ern/42/release-notification.xsd"
    )
    assert ddex_schema.schema.name == "release-notification.xsd"
    assert "ern" in ddex_schema.schema.namespaces.keys()


def test_download_ddex_xsd_to_valid_object() -> None:
    ddex_schema = load_ddex_xsd_schema(
        path="http://service.ddex.net/xml/ern/42/release-notification.xsd"
    )
    assert ddex_schema.schema.name == "release-notification.xsd"
    assert "ern" in ddex_schema.schema.namespaces.keys()


def test_raise_if_not_xsd_schema() -> None:
    with pytest.raises(DDEXException):
        load_ddex_xsd_schema(path="tests/assets/content/test-content.txt")


def test_load_ddex_xsd_to_invalid_object() -> None:
    assert False


def test_load_ddex_xml_to_valid_object() -> None:
    assert False


def test_load_invalid_ddex_xml_to_object_fails() -> None:
    assert False


def test_ddex_object_to_xml() -> None:
    assert False


def test_ddex_object_to_json() -> None:
    assert False


def test_json_to_ddex_object() -> None:
    assert False


def test_create_ddex_object() -> None:
    assert False
