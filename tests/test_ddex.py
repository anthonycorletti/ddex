import pytest

from ddex import load_ddex_xsd_schema, xml_to_ddex
from ddex.const import _DDEX_CACHE_DIR
from ddex.exc import DDEXException


def test_load_ddex_xsd_to_valid_object() -> None:
    ddex_schema = load_ddex_xsd_schema(
        path="tests/assets/schemas/ern/4.2/release-notification.xsd"
    )
    assert ddex_schema.filepath.endswith(
        "tests/assets/schemas/ern/4.2/release-notification.xsd"
    )
    assert ddex_schema.xsd.name == "release-notification.xsd"
    assert "ern" in ddex_schema.xsd.namespaces.keys()


def test_download_ddex_xsd_to_valid_object() -> None:
    ddex_schema = load_ddex_xsd_schema(
        path="http://service.ddex.net/xml/ern/42/release-notification.xsd"
    )
    assert (
        ddex_schema.filepath == f"{_DDEX_CACHE_DIR}/xml/ern/42/release-notification.xsd"
    )
    assert ddex_schema.xsd.name == "release-notification.xsd"
    assert "ern" in ddex_schema.xsd.namespaces.keys()


def test_raise_if_not_xsd_schema() -> None:
    with pytest.raises(DDEXException):
        load_ddex_xsd_schema(path="tests/assets/content/test-content.txt")


def test_load_ddex_xml_to_valid_object() -> None:
    ddex = xml_to_ddex(path="tests/assets/content/ern/4.2/Audio.xml")
    assert ddex.content is not None and ddex.schema is not None
    assert ddex.schema.xsd.name == "release-notification.xsd"
    assert "ern" in ddex.schema.xsd.namespaces.keys()
    root = ddex.content.getroot()
    assert root.attrib["{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"] == (
        "http://ddex.net/xml/ern/42 http://ddex.net/xml/ern/42/release-notification.xsd"
    )
    assert root.attrib["ReleaseProfileVersionId"] == "Audio"
    assert root.attrib["LanguageAndScriptCode"] == "en"
    ddex.assert_valid()


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
