import os
from typing import Dict, Optional
from urllib.request import urlretrieve
from uuid import UUID
from xml.etree import ElementTree

import xmlschema
from xmlschema.validators.schemas import XMLSchemaBase

from ddex.exc import DDEXException


class DDEXSchema:
    def __init__(self, schema: XMLSchemaBase) -> None:
        self.schema = schema


class DDEXDocument:
    def __init__(self, id: UUID, ddex_schema: DDEXSchema) -> None:
        pass

    def to_xml(self, output_file: Optional[str] = None) -> str:
        pass

    def to_json(self, output_file: Optional[str] = None) -> str:
        pass

    def to_dict(self) -> Dict:
        pass


def _download_remote_file(url: str) -> str:
    filename = os.path.basename(url)
    urlretrieve(url, filename)
    return filename


def _path_is_url(path: str) -> bool:
    return path.startswith("http")


# def _is_xsd(path: str) -> bool:
#     return path.endswith(".xsd")


def load_ddex_xsd_schema(path: str) -> DDEXSchema:
    filepath = path
    if _path_is_url(path):
        filepath = _download_remote_file(path)

    try:
        xsd_content = xmlschema.XMLSchema(filepath)
    except (xmlschema.XMLSchemaException, ElementTree.ParseError) as e:
        raise DDEXException(e)
    return DDEXSchema(schema=xsd_content)


def xml_to_ddex(path: str, schema: DDEXSchema) -> DDEXDocument:
    pass


def json_to_ddex(path: str, schema: DDEXSchema) -> DDEXDocument:
    pass


def dict_to_ddex(data: Dict, schema: DDEXSchema) -> DDEXDocument:
    pass
