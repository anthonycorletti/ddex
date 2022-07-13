from typing import Dict, Optional
from uuid import UUID


class DDEXSchema:
    def __init__(self) -> None:
        pass


class DDEX:
    def __init__(self, id: UUID, ddex_schema: DDEXSchema) -> None:
        pass

    def to_xml(self, output_file: Optional[str] = None) -> str:
        pass

    def to_json(self, output_file: Optional[str] = None) -> str:
        pass

    def to_dict(self) -> Dict:
        pass


def _load_file(path: str) -> str:
    pass


def load_ddex_xsd_file(path: str) -> DDEXSchema:
    pass


def load_ddex_xml_file(path: str, schema: DDEXSchema) -> DDEX:
    pass


def load_ddex_json_file(path: str, schema: DDEXSchema) -> DDEX:
    pass


def load_ddex_dict(data: Dict, schema: DDEXSchema) -> DDEX:
    pass
