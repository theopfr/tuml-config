import re
import string
from exeptions import LexerExeption
from tokens import Token, TokenType


class Lexer:
    def __init__(self, config_string: str) -> list:
        self.config_string = config_string
        self.current_position = 0
        self.current_char = self.config_string[self.current_position]

        self.tokens = []
        
    def error(self, message: str) -> None:
        """ Raises a lexer error. """

        raise LexerExeption(message)

    def set_token(self, token_type: TokenType, value: str) -> None:
        """ Adds a new token to the token list and resets the current token value. """

        self.tokens.append(Token(token_type, value))

    def advance(self) -> None:
        """ Advances to the next character and checks if the input string has ended. """

        self.current_position += 1
        if self.current_position > len(self.config_string) - 1:
            self.current_char = "EOF"
        else:
            self.current_char = self.config_string[self.current_position]

    def build_key(self) -> str:
        """ Builds a config-key out of the characters in the input string. """

        allowed_characters = string.ascii_lowercase + string.ascii_uppercase + "0123456789_"

        result = ""
        while self.current_char != ":":
            if self.current_char not in allowed_characters:
                self.error("Unexpected character in key! Only lower- and upper-case letters are allowed!")

            result += self.current_char
            self.advance()

        return result

    def build_number(self) -> str:
        """ Builds an interger or float out of the characters in the input string. """

        allowed_characters = "0123456789.eE-+"

        result = self.current_char
        self.advance()

        while self.current_char in allowed_characters:
            if self.current_char in ".eE-+":
                allowed_characters.replace(self.current_char, "")

            result += self.current_char
            self.advance()

        # check if the result is a valid int or float
        try:
            float(result)
        except:
            self.error("Couldn't read integer or float!")

        return result

    def build_bool(self, bool_type: str) -> str:
        """ Builds a boolean ('true' or 'false') out of the characters in the input string. """
        
        result = ""
        while result != bool_type:
            result += self.current_char
            self.advance()

        return result

    def build_string(self) -> str:
        """ Builds a string without '"' out of the characters in the input string. """

        # advance to skip the opening quotation marks
        self.advance()

        result = ""
        while self.current_char != '"':
            if self.current_char == "EOF":
                self.error("Expected closing quotes!")
            result += self.current_char
            self.advance()

        # advance to skip the ending quotation marks
        self.advance()

        return result
        
    def tokenize(self):
        """ Creates tokens from the characters in the input string and adds them to the token list. """

        while self.current_char != "EOF":
            #print(self.tokens)
            # ignore spaces outside strings
            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char == "t": # TODO fix
                if self.config_string[self.current_position:self.current_position + 4] == "true":
                    self.set_token(TokenType.BOOL, self.build_bool("true"))
                    continue

            elif self.current_char == "f": # TODO fix
                if self.config_string[self.current_position:self.current_position + 5] == "false":
                    self.set_token(TokenType.BOOL, self.build_bool("false"))
                    continue

            if self.current_char.isalpha():
                self.set_token(TokenType.KEY, self.build_key())

            elif self.current_char == '"':
                self.set_token(TokenType.STRING, self.build_string())

            elif self.current_char.isdigit() or re.match("[\.\-\+]", self.current_char):
                self.set_token(TokenType.INTEGER, self.build_number())

            elif self.current_char == ":":
                self.set_token(TokenType.EOK, ":")
                self.advance()

            elif self.current_char == ";":
                self.set_token(TokenType.EOE, ";")
                self.advance()

            elif self.current_char == "[":
                self.set_token(TokenType.LIST_START, "[")
                self.advance()

            elif self.current_char == "]":
                self.set_token(TokenType.LIST_END, "]")
                self.advance()

            elif self.current_char == ",":
                self.set_token(TokenType.LIST_DELIM, ",")
                self.advance()

            elif self.current_char == "(":
                self.set_token(TokenType.SECTION_START, "(")
                self.advance()

            elif self.current_char == ")":
                self.set_token(TokenType.SECTION_END, ")")
                self.advance()

            continue

        return self.tokens


""" example

config2 = '''
    myInt: 2; 
    myString: "hi im ron"; 
    mySub: ( mySubkey: "sub test"; list: [5, 8]; ); 
    myList: ["a", 2, 3,
        ( 
            subAgain: "lol"; 
            subSecond: "re";
        ), 0
    ];
    last: "the end";
    myBool: false;
'''

config = '''
    myInt: .20;
    mySting: "hello test";
    myList: ["first item", "second item", 2];
    mySection: (
        subString: "sub key";
        subInt: 202;
    );
'''

lexer = Lexer(config2)
for e in lexer.tokenize():
    print(e)
"""
