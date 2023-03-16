
from enum import Enum


class TokenType(Enum):
    KEY: str = "KEY"
    STRING: str = "STRING"
    NUMBER: str = "NUMBER"
    BOOL: str = "BOOL"
    LIST_START: str = "["
    LIST_END: str = "]"
    LIST_DELIM: str = ","
    SECTION_START: str = "("
    SECTION_END: str = ")"
    
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
        return self.token_value