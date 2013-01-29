import unittest

from pie.type import *
from pie.reader import Reader

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
class SymbolTestCase(unittest.TestCase):
    def test_define(self):
        ret = Reader('(define a 1)').read()
        self.assertListEqual(ret, [sym_define, 'a', 1])
    def test_if(self):
        ret = Reader('(if a #t #f)').read()
        self.assertListEqual(ret, [sym_if, 'a', True, False])
    def test_begin(self):
        ret = Reader('(begin (print "Hello World!") (abs -42))').read()
        self.assertEqual(ret[0], sym_begin)
