
from enum import Enum


class TokenType(Enum):
    KEY = "KEY"
    STRING = "STRING"
    INTEGER = "INTEGER"
    LIST_START = "LIST_START"
    LIST_END = "LIST_END"
    SECTION_START = "SECTION_START"
    SECTION_END = "SECTION_END"
    EOF = "EOF"


class Token:
    def __init__(self, type_: str, value) -> None:
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        return f"Token( '{self.type_}', '{self.value}' )"

    def __repr__(self) -> str:
        return self.__str__()