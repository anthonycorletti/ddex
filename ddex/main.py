import os
from typing import Dict, Optional
from urllib.parse import urlparse
from urllib.request import urlretrieve
from uuid import UUID, uuid4
from xml.etree.ElementTree import ParseError

import xmlschema
from lxml import etree
from lxml.etree import ElementTree
from xmlschema.validators.schemas import XMLSchemaBase

from ddex.const import _DDEX_CACHE_DIR, _SCHEMA_LOCATION
from ddex.exc import DDEXException


class DDEXSchema:
    def __init__(self, filepath: str, xsd: XMLSchemaBase) -> None:
        self.xsd = xsd
        self.filepath = filepath


class DDEXDocument:
    def __init__(
        self,
        schema: DDEXSchema,
        content: ElementTree,
        id: Optional[UUID] = None,
    ) -> None:
        self.id = id or uuid4()
        self.schema = schema
        self.content = content

    def assert_valid(self) -> None:
        schema_tree = etree.parse(self.schema.filepath)
        schema = etree.XMLSchema(schema_tree)
        schema.assertValid(self.content.getroot())

    def to_xml(self, output_file: Optional[str] = None) -> str:
        pass

    def to_json(self, output_file: Optional[str] = None) -> str:
        pass

    def to_dict(self) -> Dict:
        pass


def _download_remote_file(url: str, ignore_ddex_cache: bool = False) -> str:
    parsed_url = urlparse(url=url)
    filename = f"{_DDEX_CACHE_DIR}/{parsed_url.path[1:]}"
    dirs = os.path.dirname(filename)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if not os.path.exists(filename) or ignore_ddex_cache:
        urlretrieve(url=url, filename=filename)
    return filename


def _path_is_url(path: str) -> bool:
    return path.startswith("http")


def load_ddex_xsd_schema(path: str, ignore_ddex_cache: bool = False) -> DDEXSchema:
    filepath = path
    if _path_is_url(path):
        filepath = _download_remote_file(url=path, ignore_ddex_cache=ignore_ddex_cache)

    try:
        xsd_content = xmlschema.XMLSchema(filepath)
    except (xmlschema.XMLSchemaException, ParseError) as e:
        raise DDEXException(e)
    return DDEXSchema(filepath=filepath, xsd=xsd_content)


def xml_to_ddex(path: str, schema: Optional[DDEXSchema] = None) -> DDEXDocument:
    content = etree.parse(path)
    root = content.getroot()
    if schema is None:
        schema = dict(root.items()).get(_SCHEMA_LOCATION)
        if not schema:
            raise DDEXException("No schema found in XML.")
        schema_path = [
            v for v in schema.split() if os.path.basename(v).endswith(".xsd")
        ]
        if not schema_path:
            raise DDEXException("No schema path found in XML.")
        _ddex_schema = load_ddex_xsd_schema(path=schema_path[-1])
    else:
        _ddex_schema = schema
    _ddex_schema.xsd.validate(content)
    return DDEXDocument(schema=_ddex_schema, content=content)


def json_to_ddex(path: str, schema: Optional[DDEXSchema] = None) -> DDEXDocument:
    pass


def dict_to_ddex(data: Dict, schema: Optional[DDEXSchema] = None) -> DDEXDocument:
    pass
