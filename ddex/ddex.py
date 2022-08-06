import json
import os
from typing import Dict, Optional
from urllib.parse import urlparse
from urllib.request import urlretrieve
from uuid import UUID, uuid4
from xml.etree.ElementTree import ParseError

import xmlschema
import xmltodict
from lxml import etree
from lxml.etree import ElementTree
from xmlschema.validators.schemas import XMLSchemaBase

from ddex.const import _DDEX_CACHE_DIR, _SCHEMA_LOCATION
from ddex.exc import DDEXException


class DDEXSchema:
    """DDEXSchema."""

    def __init__(self, filepath: str, xsd: XMLSchemaBase) -> None:
        """Initialize DDEXSchema.

        Args:
            filepath (str): Path to the XSD file.
            xsd (XMLSchemaBase): XMLSchema object.
        """
        self.xsd = xsd
        self.filepath = filepath


class DDEXDocument:
    """DDEXDocument."""

    def __init__(
        self,
        schema: DDEXSchema,
        content: ElementTree,
        id: Optional[UUID] = None,
    ) -> None:
        """Initalize a DDEXDocument object.

        Args:
            schema (DDEXSchema): DDEX schema object.
            content (ElementTree): DDEX content object in the form of an Elementree.
            id (Optional[UUID], optional): A document UUID. Automatically set if
                not provided.
        """
        self.id = id or uuid4()
        self.schema = schema
        self.content = content
        self.root = content.getroot()

    def assert_valid(self) -> None:
        """DDEXDocument.assert_valid.

        Asserts that the DDEX document is valid.
        """
        schema_tree = etree.parse(self.schema.filepath)
        schema = etree.XMLSchema(schema_tree)
        schema.assertValid(self.root)

    def to_xml(self, output_file: str) -> str:
        """DDEXDocument.to_xml.

        Args:
            output_file (str): The path to the output file.

        Returns:
            str: The path to the output file.
        """
        self.content.write(output_file, encoding="utf-8", xml_declaration=True)
        return output_file

    def to_json(self, output_file: str) -> str:
        """DDEXDocument.to_json.

        Args:
            output_file (str): The path to the output file.

        Returns:
            str: The path to the output file.
        """
        content_dict = self.to_dict()
        with open(output_file, "w") as f:
            json.dump(content_dict, f)
        return output_file

    def to_dict(self) -> Dict:
        """DDEXDocument.to_dict.

        Returns:
            Dict: The DDEX document as a dictionary.
        """
        return xmltodict.parse(etree.tostring(self.content))


def _download_remote_schema(url: str, ignore_ddex_cache: bool = False) -> str:
    """_download_remote_schema.

    Private function to download a remote schema.

    Args:
        url (str): The URL location of the schema.
        ignore_ddex_cache (bool, optional): Option to ignore the local cache.
            Defaults to False.

    Returns:
        str: The path to the downloaded schema.
    """
    parsed_url = urlparse(url=url)
    filename = f"{_DDEX_CACHE_DIR}/{parsed_url.path[1:]}"
    dirs = os.path.dirname(filename)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if not os.path.exists(filename) or ignore_ddex_cache:
        urlretrieve(url=url, filename=filename)
    return filename


def _path_is_url(path: str) -> bool:
    """_path_is_url.

    Args:
        path (str): The path to check.

    Returns:
        bool: Whether the path is a URL.
    """
    return path.startswith("http")


def load_ddex_xsd_schema(path: str, ignore_ddex_cache: bool = False) -> DDEXSchema:
    """load_ddex_xsd_schema.

    Args:
        path (str): The path to the XSD file.
        ignore_ddex_cache (bool, optional): Option to ignore the local cache.
            Defaults to False.

    Raises:
        DDEXException: The XSD file could not be loaded.

    Returns:
        DDEXSchema: The DDEXSchema object.
    """
    filepath = path
    if _path_is_url(path):
        filepath = _download_remote_schema(
            url=path, ignore_ddex_cache=ignore_ddex_cache
        )

    try:
        xsd_content = xmlschema.XMLSchema(filepath)
    except (xmlschema.XMLSchemaException, ParseError) as e:
        raise DDEXException(e)
    return DDEXSchema(filepath=filepath, xsd=xsd_content)


def _set_ddex_schema(
    root: etree._Element, schema: Optional[DDEXSchema] = None
) -> DDEXSchema:
    """_set_ddex_schema.

    Private function to set the DDEXSchema.

    Args:
        root (etree._Element): The root of the DDEX document.
        schema (Optional[DDEXSchema], optional): The DDEXSchema. Defaults to None.

    Raises:
        DDEXException: No DDEXSchema found.

    Returns:
        DDEXSchema: The DDEXSchema object.
    """
    if schema:
        return schema
    schema = dict(root.items()).get(_SCHEMA_LOCATION)
    if not schema:
        raise DDEXException("No schema found in XML.")
    return load_ddex_xsd_schema(path=schema.split()[-1])


def xml_to_ddex(path: str, schema: Optional[DDEXSchema] = None) -> DDEXDocument:
    """xml_to_ddex.

    Args:
        path (str): The path to the XML file.
        schema (Optional[DDEXSchema], optional): The DDEXSchema object.
            Defaults to None.

    Returns:
        DDEXDocument: The DDEXDocument object.
    """
    content = etree.parse(path)
    root = content.getroot()
    _schema = _set_ddex_schema(root=root, schema=schema)
    _schema.xsd.validate(content)
    return DDEXDocument(schema=_schema, content=content)


def json_to_ddex(path: str, schema: Optional[DDEXSchema] = None) -> DDEXDocument:
    """json_to_ddex.

    Args:
        path (str): The path to the JSON file.
        schema (Optional[DDEXSchema], optional): The DDEXSchema object.
            Defaults to None.

    Returns:
        DDEXDocument: The DDEXDocument object.
    """
    json_file = open(path)
    json_data = json.load(json_file)
    return dict_to_ddex(data=json_data, schema=schema)


def dict_to_ddex(data: Dict, schema: Optional[DDEXSchema] = None) -> DDEXDocument:
    """dict_to_ddex.

    Args:
        data (Dict): The data to convert to a DDEXDocument.
        schema (Optional[DDEXSchema], optional): The DDEXSchema object.
            Defaults to None.

    Returns:
        DDEXDocument: The DDEXDocument object.
    """
    data_xml_bytes = xmltodict.unparse(data).encode("utf8")
    root = etree.fromstring(data_xml_bytes)
    schema = _set_ddex_schema(root=root, schema=schema)
    content = ElementTree(root)
    return DDEXDocument(content=content, schema=schema)


def generate_ddex_module(input_path: str, module_output_path: str) -> None:
    """generate_ddex_module.

    Generate a python file that contains the DDEX classes.

    Args:
        input_path (str): The path to the XML or XSD file.
        module_output_path (str): The path to the python file (absolute module path).
    """
    os.system(f"xsdata generate --package {module_output_path} {input_path}")
