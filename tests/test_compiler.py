import os
import dis
import unittest

from pie.type import *
from pie.compiler import save_pyc
from pie.compiler import Compiler

class SimpleCompilerTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def test_func_call(self):
        c = Compiler()
        c.compile(['ord', 'a'])
        self.assertEqual(eval(c.dump()), 97)
    def test_nest_func_call(self):
        c = Compiler()
        c.compile(['abs', ['max', -100, -42]])
        self.assertEqual(eval(c.dump()), 42)
    def test_define(self):
        c = Compiler()
        c.compile([sym_define, Symbol('answer'), -42])
        c.compile(['abs', Symbol('answer')])
        self.assertEqual(eval(c.dump()), 42)
    def test_if(self):
        c = Compiler()
        c.compile([sym_if, True, "True!"])
        self.assertEqual(eval(c.dump()), "True!")
        c = Compiler()
        c.compile([sym_if, True, "True!", "False!"])
        self.assertEqual(eval(c.dump()), "True!")
        c = Compiler()
        c.compile([sym_if, False, "True!", "False!"])
        self.assertEqual(eval(c.dump()), "False!")
    def test_begin(self):
        c = Compiler()
        c.compile([sym_begin, [sym_define, Symbol('answer'), 42],
            ['abs', Symbol('answer')]])
        self.assertEqual(eval(c.dump()), 42)

class PycTestCase(unittest.TestCase):
    def setUp(self):
        c = Compiler()
        c.compile(['ord', 'a'])
        self.co = c.dump()
    def test_pyc_dump(self):
        save_pyc(self.co, 'justtest123.pyc')
        open('justtest123.pyc')
    def tearDown(self):
        os.remove('justtest123.pyc')
