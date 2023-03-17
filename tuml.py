from lexer import Lexer
from tokens import Token, TokenType
from exeptions import ParserExeption, TumlFileExeption
from utils import load_file


def error(message: str) -> None:
    """ Raises a parser error. """

    raise ParserExeption(message)


def section_end_idx(tokens: list[Token], current_position: int) -> int:
    """ Finds the index of the token which end the outermost section indicated by "]" """

    idx = 0
    nested_section_levels = 1
    for idx, current_token in enumerate(tokens[current_position + 1:]):

        if current_token.token_type == TokenType.SECTION_START:
            nested_section_levels += 1
        elif current_token.token_type == TokenType.SECTION_END:
            nested_section_levels -= 1

        if nested_section_levels == 0:
            break

    return idx + current_position + 1


def list_end_idx(tokens: list[Token], current_position: int) -> int:
    """ Finds the index of the token which end the outermost section indicated by ")" """

    idx = 0
    nested_section_levels = 1
    for idx, current_token in enumerate(tokens[current_position + 1:]):

        if current_token.token_type == TokenType.LIST_START:
            nested_section_levels += 1
        elif current_token.token_type == TokenType.LIST_END:
            nested_section_levels -= 1

        if nested_section_levels == 0:
            break

    return idx + current_position + 1


def parse_list(tokens: list[Token]) -> list:
    """ Recursively parses tokens into a Python list. """

    expected_types = [TokenType.STRING, TokenType.NUMBER, TokenType.BOOL, TokenType.SECTION_START, TokenType.LIST_START, TokenType.LIST_END]
    result_list = []

    tokens.append(Token(TokenType.EOF, "EOF"))

    idx = 0
    while tokens[idx].token_value != "EOF":
        current_token = tokens[idx]
        current_token_type = current_token.token_type
        current_token_value = current_token.token_value

        # check if the token is expected, if not throw an error
        if current_token_type not in expected_types:
            error("Unexpected token!")

        # check if the token is a dict-value and append it to the list as an item
        elif current_token_type in [TokenType.STRING, TokenType.NUMBER, TokenType.BOOL]:
            expected_types = [TokenType.LIST_DELIM, TokenType.LIST_END]

            if current_token_type == TokenType.NUMBER:
                current_token_value = float(current_token_value) if not float(current_token_value).is_integer() else int(current_token_value)
            elif current_token_type == TokenType.BOOL:
                current_token_value = current_token_value == "true"

            result_list.append(current_token_value)

        # check if it is the token for station a new list ("[") and parse the list with all it's tokens recursively
        elif current_token_type == TokenType.LIST_START:
            # get the index of the token which ends the list and extract all the tokens from the current position until there
            section_ends = list_end_idx(tokens, idx)
            sub_tokens = tokens[idx + 1:section_ends]
            # recursive descent on the extracted list
            result_list.append(parse_list(sub_tokens))

            # the closing bracket token will be skipped by jumping to the end of the list, continue from there
            expected_types = [TokenType.LIST_DELIM]
            idx = section_ends

        # check if it is the token for station a new section ("(") and parse the section with all it's tokens recursively
        elif current_token_type == TokenType.SECTION_START:
            # get the index of the token which ends the section and extract all the tokens from the current position until there
            section_ends = section_end_idx(tokens, idx)
            sub_tokens = tokens[idx + 1:section_ends]
            # recursive descent on the extracted section and append it to the list
            result_list.append(parse(sub_tokens))

            # the closing parentheses token will be skipped by jumping to the end of the section, continue from there
            expected_types = [TokenType.LIST_DELIM, TokenType.LIST_END]
            idx = section_ends

        elif current_token_type == TokenType.LIST_DELIM:
            expected_types = [TokenType.STRING, TokenType.NUMBER, TokenType.BOOL, TokenType.SECTION_START, TokenType.LIST_START]

        idx += 1

    return result_list


def parse(tokens: list[Token]) -> dict:
    """ Recursively parses the tokens into a Python dict. """

    expected_types = [TokenType.KEY]
    last_key = None
    result_dict = {}

    tokens.append(Token(TokenType.EOF, "EOF"))

    idx = 0
    while True:
        current_token = tokens[idx]
        current_token_type = current_token.token_type
        current_token_value = current_token.token_value

        # check if the token is expected, if not throw an error
        if current_token_type not in expected_types:
            print(current_token_type, expected_types)
            error("Unexpected token!")

        # check if it is the End-Of-File token and if so break
        elif current_token_type == TokenType.EOF:
            break
        
        # check if the token is a key and create a entry in the dict for it
        elif current_token_type == TokenType.KEY:
            result_dict[current_token_value] = None
            last_key = current_token_value
            expected_types = [TokenType.EOK]

        # check if it is the End-Of-Key token (":") and if so expect a dict-value token
        elif current_token_type == TokenType.EOK:
            expected_types = [TokenType.STRING, TokenType.NUMBER, TokenType.BOOL, TokenType.LIST_START, TokenType.SECTION_START]

        # check if the token is a dict-value
        elif current_token_type in [TokenType.STRING, TokenType.NUMBER, TokenType.BOOL]:
            
            if current_token_type == TokenType.NUMBER:
                current_token_value = float(current_token_value) if not float(current_token_value).is_integer() else int(current_token_value)
            elif current_token_type == TokenType.BOOL:
                current_token_value = current_token_value == "true"

            result_dict[last_key] = current_token_value
            expected_types = [TokenType.EOE]

        # check if it is the End-Of-Expression token (";")
        elif current_token_type == TokenType.EOE:
            expected_types = [TokenType.KEY, TokenType.SECTION_END, TokenType.EOF]

        # check if it is the token for starting a new list ("[") and parse the list with all it's tokens recursively
        elif current_token_type == TokenType.LIST_START:
            # get the index of the token which ends the list and extract all the tokens from the current position until there
            list_ends = list_end_idx(tokens, idx)
            sub_tokens = tokens[idx + 1:list_ends]
            # recursive descent on the extracted list
            result_dict[last_key] = parse_list(sub_tokens)

            # the closing bracket token will be skipped by jumping to the end of the list, continue from there
            expected_types = [TokenType.EOE]
            idx = list_ends

        # check if it is the token for station a new section ("(") and parse the section with all it's tokens recursively
        elif current_token_type == TokenType.SECTION_START:
            # get the index of the token which ends the section and extract all the tokens from the current position until there
            section_ends = section_end_idx(tokens, idx)
            sub_tokens = tokens[idx + 1:section_ends]
            # recursive descent on the extracted section
            result_dict[last_key] = parse(sub_tokens)

            # the closing parentheses token will be skipped by jumping to the end of the section, continue from there
            expected_types = [TokenType.EOE]
            idx = section_ends
            
        idx += 1

    return result_dict


def loads(config_string: str) -> dict:
    """ parses a tuml string to a Python dict """
    tokens = Lexer(config_string).tokenize()
    return parse(tokens)


def load(config_file: str) -> dict:
    """ loads the content of a tuml file and parses it to a Python dict """

    if not config_file.endswith(".tuml"):
        raise TumlFileExeption("Expected file with '.tuml' extension!")

    config_string = load_file(config_file)
    return loads(config_string)

