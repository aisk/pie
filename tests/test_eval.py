import unittest

from pie.builtin import *
from pie.reader import Reader
from pie.compiler import Compiler

class EvalTestCase(unittest.TestCase):
    def test_func(self):
        src = """
        (abs -42)
        """
        r = Reader(src).read()
        c = Compiler()
        c.compile(r)
        self.assertEqual(eval(c.dump()), 42)
