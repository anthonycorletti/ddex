import os

from lxml import etree

_SCHEMA_LOCATION = etree.QName(
    "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"
)

_DDEX_CACHE_DIR = f"{os.getenv('HOME', '/root')}/.ddex"
