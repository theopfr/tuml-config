import unittest
from test_cases import *

import sys
sys.path.append("..")

import tuml

class TestParser(unittest.TestCase):
    def test1(self):
        parsed = tuml.loads(success_case_1["input"])
        self.assertEqual(parsed, success_case_1["expected"])

    def test2(self):
        parsed = tuml.loads(success_case_2["input"])
        self.assertEqual(parsed, success_case_2["expected"])


if __name__ == "__main__":
    unittest.main()