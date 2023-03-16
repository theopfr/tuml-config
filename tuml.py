from lexer import Lexer
from tokens import Token, TokenType
from exeptions import ParserExeption


class Parser:
    def __init__(self) -> None:
        pass

    def error(self, message: str) -> None:
        """ Raises a parser error. """

        raise ParserExeption(message)

    def section_end_idx(self, tokens: list[Token], current_position: int) -> int:
        nested_section_levels = 1
        for idx, current_token in enumerate(tokens[current_position + 1:]):

            if current_token.token_type == TokenType.SECTION_START:
                nested_section_levels += 1
            elif current_token.token_type == TokenType.SECTION_END:
                nested_section_levels -= 1

            if nested_section_levels == 0:
                break

        return idx + current_position + 1

    def list_end_idx(self, tokens: list[Token], current_position: int) -> int:
        nested_section_levels = 1
        for idx, current_token in enumerate(tokens[current_position + 1:]):

            if current_token.token_type == TokenType.LIST_START:
                nested_section_levels += 1
            elif current_token.token_type == TokenType.LIST_END:
                nested_section_levels -= 1

            if nested_section_levels == 0:
                break

        return idx + current_position + 1

    def parse_list(self, tokens: list[Token]) -> list:
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
                self.error("Unexpected token!")

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
                section_ends = self.list_end_idx(tokens, idx)
                sub_tokens = tokens[idx + 1:section_ends]
                # recursive descent on the extracted list
                result_list.append(self.parse_list(sub_tokens))

                # the closing bracket token will be skipped by jumping to the end of the list, continue from there
                expected_types = [TokenType.LIST_DELIM]
                idx = section_ends

            # check if it is the token for station a new section ("(") and parse the section with all it's tokens recursively
            elif current_token_type == TokenType.SECTION_START:
                # get the index of the token which ends the section and extract all the tokens from the current position until there
                section_ends = self.section_end_idx(tokens, idx)
                sub_tokens = tokens[idx + 1:section_ends]
                # recursive descent on the extracted section and append it to the list
                result_list.append(self.parse(sub_tokens))

                # the closing paranthesis token will be skipped by jumping to the end of the section, continue from there
                expected_types = [TokenType.LIST_DELIM, TokenType.LIST_END]
                idx = section_ends

            elif current_token_type == TokenType.LIST_DELIM:
                expected_types = [TokenType.STRING, TokenType.NUMBER, TokenType.BOOL, TokenType.SECTION_START, TokenType.LIST_START]

            idx += 1

        return result_list

    def parse(self, tokens: list[Token]) -> dict:
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
                self.error("Unexpected token!")

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
                list_ends = self.list_end_idx(tokens, idx)
                sub_tokens = tokens[idx + 1:list_ends]
                # recursive descent on the extracted list
                result_dict[last_key] = self.parse_list(sub_tokens)

                # the closing bracket token will be skipped by jumping to the end of the list, continue from there
                expected_types = [TokenType.EOE]
                idx = list_ends

            # check if it is the token for station a new section ("(") and parse the section with all it's tokens recursively
            elif current_token_type == TokenType.SECTION_START:
                # get the index of the token which ends the section and extract all the tokens from the current position until there
                section_ends = self.section_end_idx(tokens, idx)
                sub_tokens = tokens[idx + 1:section_ends]
                # recursive descent on the extracted section
                result_dict[last_key] = self.parse(sub_tokens)

                # the closing paranthesis token will be skipped by jumping to the end of the section, continue from there
                expected_types = [TokenType.EOE]
                idx = section_ends
                
            idx += 1

        return result_dict

    def load(self, config: str) -> dict:
        # TODO load file here

        tokens = Lexer(config).tokenize()
        parsed = self.parse(tokens) 


        return parsed


config2 = '''
myKey: "myValue";
myList: ["myItem", 2];
mySection: (
    mySectionKey: "mySectionValue";
    mySectionList: [1, 2, [(a: 1;)]];
);
'''

config1 = '''
myInt: 9;
mySection: (
    mySectionString: "sub";
    mySubSection: (
        mySubInt: false;
        gett: "hi";
    );
    that: "this";
);
here: "there";

b: (
    inner: [
        (
            name: "ted";
            age: 21;
        ),
        (
            name: "bill";
            age: 33;
        )
    ];
    mhm: -1;
); 
'''
# myList: [1, [2, 3, (a: "0"; b: (u: "1"; u2: "2"; u3: ["l", "o", "l"];);)]]

config0 = '''
section1: (
    section2: (
        section3: (
            section4: (
                inner: "lol";
                list: [
                    [
                        [

                        ]
                    ]
                ];
            );
        );
    );
);
'''

config = '''
    testString: "test string";
    testInt: 10;
    testFloat: -2e-3;
    testTrue: true;
    testFalse: false;
    testSection: (
        sectionString: "test string";
        sectionList: [1, 2, 3];
    );
    testList: [1, 2, "test string", (
        listSectionInt: 3;
        listSectionBool: true;
    )];
    lastTestFloat: .3E-7;
    l: [[1], [2], [3]];
    l2: [
        [
            [2]
        ]
    ];
'''



# TODO replace class with just functions

#parsed = Parser().load(config)
#print(parsed)
