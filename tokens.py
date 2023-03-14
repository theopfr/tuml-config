
from enum import Enum


class TokenType(Enum):
    KEY: str = "KEY"
    STRING: str = "STRING"
    INTEGER: str = "INTEGER"
    BOOL: str = "BOOL"
    LIST_START: str = "LIST_START"
    LIST_END: str = "LIST_END"
    LIST_DELIM: str = "LIST_DELIM"
    SECTION_START: str = "SECTION_START"
    SECTION_END: str = "SECTION_END"
    
    # end of key
    EOK: str = ":"
    # end of expression (key-value pair)
    EOE: str = ";"
    # end of file
    EOF: str = "EOF"


class Token:
    def __init__(self, token_type: TokenType, token_value: str) -> None:
        self.token_type = token_type
        self.token_value = token_value

    def __str__(self) -> str:
        return f"Token( '{self.token_type}', '{self.token_value}' )"

    def __repr__(self) -> str:
        return self.__str__()