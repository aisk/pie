import unittest

from pie.reader import Reader
from pie.builtin import *

class SimpleReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.ret = Reader('(+ 1 (- 2 "hello"))').read()
    def test_reader(self):
        self.assertEqual(len(self.ret), 3)
        self.assertEqual(len(self.ret[2]), 3)
    def test_type(self):
        self.assertIsInstance(self.ret[0], Symbol)
        self.assertIsInstance(self.ret[1], int)
        self.assertIsInstance(self.ret[2], list)
        self.assertIsInstance(self.ret[2][2], str)

