import re
import string
from expections import ParserExecption
from tokens import Token, TokenType


class Lexer:
    def __init__(self, text_input: str) -> list:
        self.text_input = text_input
        self.current_position = 0
        self.current_char = self.text_input[self.current_position]

        self.tokens = []

        self.current_token_value = ""

        self.inside_integer = False
        self.inside_section = False
        self.nexted_section_level = 0

        self.expect_value = False
        self.expect_key = True

    def error(self, message: str) -> None:
        """ Raises a parser error. """

        raise ParserExecption(message)

    def set_token(self, token_type: TokenType, value: str) -> None:
        """ Adds a new token to the token list and resets the current token value. """

        self.tokens.append(Token(token_type, value))
        self.current_token_value = ""

    def advance(self) -> None:
        """ Advances to the next character and checks if the input string has ended. """

        self.current_position += 1
        if self.current_position > len(self.text_input) - 1:
            self.current_char = "EOF"
        else:
            self.current_char = self.text_input[self.current_position]

    def build_key(self) -> str:
        """ Builds a config-key out of the characters in the input string. """

        allowedCharacters = string.ascii_lowercase + string.ascii_uppercase
        result = ""
        while self.current_char != ":":
            if self.current_char not in allowedCharacters:
                self.error("Unexpected character in key! Only lower- and upper-case letters are allowed!")

            result += self.current_char
            self.advance()

        return result

    def build_number(self) -> str:
        """ Builds an interger or float out of the characters in the input string. """

        # chatgpt generated regex: ^-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?$
        number_ending_chars = [";", ",", "]"]

        result = ""
        while self.current_char not in number_ending_chars:
            result += self.current_char
            self.advance()

        # check if the result is a valid int or float
        try:
            float(result)
        except:
            self.error("Couldn't read integer or float!")

        return result

    def build_string(self) -> str:
        """ Builds a string without '"' out of the characters in the input string. """

        # advance to skip the opening quotation marks
        self.advance()

        result = ""
        while self.current_char != '"':
            result += self.current_char
            self.advance()

        # advance to skip the ending quotation marks
        self.advance()

        return result
        
    def tokenize(self):
        """ Creates tokens from the characters in the input string and adds them to the token list. """

        while self.current_char != "EOF":
            
            # ignore spaces outside strings
            if self.current_char.isspace():
                self.advance()
                continue

            # if a key is expected
            if self.expect_key:

                # check if there is a closing section
                if self.current_char == ")":
                    self.set_token(TokenType.SECTION_END, ")")
                    self.advance()
                    continue
                
                # check if there is a closing list
                elif self.current_char == "]":
                    self.set_token(TokenType.LIST_END, "]")
                    self.advance()
                    continue
                
                # check if there is a closing key-value pair (TODO what's this again?)
                elif self.current_char == ";":
                    self.advance()
                    continue
                    
                # get key
                self.set_token(TokenType.KEY, self.build_key())

                # check if the key has ended indicated by ":"
                if self.current_char == ":":
                    self.expect_key = False
                    self.expect_value = True
                    self.advance()

            # if a value is expected
            elif self.expect_value:

                # check if a string starts indicated by '"'
                if self.current_char == '"':
                    self.set_token(TokenType.STRING, self.build_string())

                # check if an integer or float starts indicated by a number, ".", "-" or "+"
                elif self.current_char.isdigit() or re.match("[\.\-\+]", self.current_char):
                    self.set_token(TokenType.INTEGER, self.build_number())

                # check if the value has ended indicated by ";"
                elif self.current_char == ";":
                    self.expect_key = True
                    self.expect_value = False
                    self.advance()

                # check if a new section starts
                elif self.current_char == "(":
                    self.expect_key = True
                    self.expect_value = False
                    self.set_token(TokenType.SECTION_START, "(")
                    self.advance()

                # check if a new list starts
                elif self.current_char == "[":
                    self.expect_key = False
                    self.expect_value = True
                    self.set_token(TokenType.LIST_START, "[")
                    self.advance()

                # check if a list has ended
                elif self.current_char == "]":
                    self.set_token(TokenType.LIST_END, "]")
                    self.advance()

                # ignore commatas in lists
                elif self.current_char == ",":
                    self.advance()

                # throw expection if any other character is encountered
                else:
                    self.error("Unexpected character!")

        return self.tokens


""" example
"""
config = '''
    myInt: 2; 
    myString: "test hi"; 
    mySub: ( mySubkey: "sub test"; list: [5, 8]; ); 
    myList: ["a", 2, 3,
        ( 
            subAgain: "lol"; 
            subSecond: "re"; 
            n: [[(a: "a";)]];
        );
    ];
    last: "the end";

'''

lexer = Lexer(config)
print(lexer.tokenize())

