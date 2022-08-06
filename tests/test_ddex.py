import os
import shutil
from unittest import mock

import pytest
from xmlschema.validators.exceptions import XMLSchemaChildrenValidationError

from ddex import load_ddex_xsd_schema, xml_to_ddex
from ddex.const import _DDEX_CACHE_DIR
from ddex.ddex import _download_remote_schema, generate_ddex_module, json_to_ddex
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
    with pytest.raises(XMLSchemaChildrenValidationError):
        xml_to_ddex(path="tests/assets/content/ern/4.2/Audio_invalid.xml")


def test_ddex_object_to_xml() -> None:
    output_file = "tests/assets/content/ern/4.2/Audio_output.xml"
    ddex = xml_to_ddex(path="tests/assets/content/ern/4.2/Audio.xml")
    result = ddex.to_xml(output_file=output_file)
    assert result.endswith(output_file)
    ddex = xml_to_ddex(path=output_file)
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
    os.remove(output_file)


def test_ddex_object_to_json() -> None:
    output_file = "tests/assets/content/Audio_output.json"
    ddex = xml_to_ddex(path="tests/assets/content/ern/4.2/Audio.xml")
    result = ddex.to_json(output_file=output_file)
    assert result.endswith(output_file)
    ddex = json_to_ddex(path=output_file)
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
    os.remove(output_file)


@mock.patch("ddex.ddex.urlretrieve", autospec=True)
def test_download_remote_schema_new_dirs(mock_urlretrieve: mock.MagicMock) -> None:
    shutil.rmtree(_DDEX_CACHE_DIR)
    _download_remote_schema(
        url="http://service.ddex.net/xml/ern/42/release-notification.xsd"
    )
    _download_remote_schema(
        url="http://service.ddex.net/xml/ern/42/release-notification.xsd",
        ignore_ddex_cache=True,
    )
    assert mock_urlretrieve.call_count == 2


def test_ddex_doc_with_missing_schema_raises() -> None:
    with pytest.raises(DDEXException):
        xml_to_ddex(path="tests/assets/content/ern/4.2/Audio_missing_schema.xml")


def test_ddex_doc_with_schema() -> None:
    ddex = xml_to_ddex(
        path="tests/assets/content/ern/4.2/Audio.xml",
        schema=load_ddex_xsd_schema(
            path="tests/assets/schemas/ern/4.2/release-notification.xsd"
        ),
    )
    ddex.assert_valid()


def test_create_ddex_module_from_xml() -> None:
    generate_ddex_module(
        input_path="tests/assets/content/ern/4.2/Audio.xml",
        module_output_path="tests.ern42.Audio",
    )
    assert os.path.exists("tests/ern42/audio/new_release_message.py")
    assert "Release" in open("tests/ern42/audio/new_release_message.py").read()
    shutil.rmtree("tests/ern42")


def test_create_ddex_module_from_xsd() -> None:
    generate_ddex_module(
        input_path="tests/assets/schemas/ern/4.2/release-notification.xsd",
        module_output_path="tests.ern42.release_notification",
    )
    assert os.path.exists("tests/ern42/release_notification/release_notification.py")
    assert (
        "Release"
        in open("tests/ern42/release_notification/release_notification.py").read()
    )
    shutil.rmtree("tests/ern42")
