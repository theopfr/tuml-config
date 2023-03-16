import unittest
from test_cases import *

import sys
sys.path.append("..")

from tuml import Parser, Lexer


class TestParser(unittest.TestCase):
    def test1(self):
        tokens = Lexer(success_case_1["input"]).tokenize()
        parsed = Parser().parse(tokens)
        self.assertEqual(parsed, success_case_1["expected"])

    def test2(self):
        tokens = Lexer(success_case_2["input"]).tokenize()
        parsed = Parser().parse(tokens)
        self.assertEqual(parsed, success_case_2["expected"])


if __name__ == "__main__":
    unittest.main()