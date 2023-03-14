from lexer import Lexer
from tokens import Token, TokenType
from exeptions import ParserExeption


class Parser:
    def __init__(self) -> None:
        # self.expected_types = [TokenType.KEY]
        self.last_key = ""

    def error(self, message: str) -> None:
        """ Raises a parser error. """

        raise ParserExeption(message)

    def eat(self) -> None:
        return

    def section_end_idx(self, tokens: list[Token], current_position: int) -> int:
        if tokens[current_position].token_value != "(":
            self.error("Expected section start!")

        nested_section_levels = 1
        for idx, current_token in enumerate(tokens[current_position + 1:]):

            if current_token.token_type == TokenType.SECTION_START:
                nested_section_levels += 1
            elif current_token.token_type == TokenType.SECTION_END:
                nested_section_levels -= 1

            if nested_section_levels == 0:
                break

        return idx + current_position + 1

    def parse(self, tokens: list[Token]) -> dict:
        expected_types = [TokenType.KEY]
        last_key = None
        result_dict = {}

        tokens.append(Token(TokenType.EOF, "EOF"))

        idx = 0
        while tokens[idx].token_value != "EOF":
            current_token = tokens[idx]
            
            #for idx, current_token in enumerate(tokens):
            print(idx, len(tokens), current_token.token_value)

            current_token_type = current_token.token_type
            current_token_value = current_token.token_value

            if current_token_type not in expected_types:
                self.error("Unexpected token!")

            elif current_token_type == TokenType.KEY:
                result_dict[current_token_value] = None
                last_key = current_token_value
                expected_types = [TokenType.EOK]

            elif current_token_type == TokenType.EOK:
                expected_types = [TokenType.STRING, TokenType.INTEGER, TokenType.BOOL, TokenType.LIST_START, TokenType.SECTION_START]

            elif current_token_type in [TokenType.STRING, TokenType.INTEGER, TokenType.BOOL]:
                result_dict[last_key] = current_token_value
                expected_types = [TokenType.EOE]

            elif current_token_type == TokenType.EOE:
                expected_types = [TokenType.KEY, TokenType.SECTION_END, TokenType.EOF]

            elif current_token_type == TokenType.SECTION_START:
                expected_types = [TokenType.KEY]

                # get the index of the token which ends the section
                section_ends = self.section_end_idx(tokens, idx)

                # extract the tokens within the section for recursive descent
                sub_tokens = tokens[idx + 1:section_ends]

                # recursive descent on the extracted section
                sub_result_dict = self.parse(sub_tokens)
                result_dict[last_key] = sub_result_dict

                # jump to the end of the section and continue from there since this part has been taken care of in the recursion
                idx = section_ends + 1

                print("\n\nSUB:", sub_tokens)
                print("\n\nTOK:", tokens)
                
            idx += 1

        return result_dict

    def load(self, config: str) -> dict:
        # TODO load file here

        tokens = Lexer(config).tokenize()
        print(tokens, "\n\n")
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
'''

config0 = '''
section1: (
    section2: (
        section3: (
            section4: (
                inner: "lol";
            );
        );
    );
);
'''


parsed = Parser().load(config0)
print(parsed)
