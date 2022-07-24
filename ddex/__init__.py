"""ddex"""

__version__ = "0.0.1-alpha"

from ddex.main import (
    DDEXDocument,
    DDEXSchema,
    dict_to_ddex,
    json_to_ddex,
    load_ddex_xsd_schema,
    xml_to_ddex,
)

__all__ = [
    "load_ddex_xsd_schema",
    "xml_to_ddex",
    "json_to_ddex",
    "dict_to_ddex",
    "DDEXDocument",
    "DDEXSchema",
]
