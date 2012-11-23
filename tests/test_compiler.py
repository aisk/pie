import os
import unittest

from pie.builtin import *
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
        c.compile(['define', Symbol('answer'), -42])
        c.compile(['abs', Symbol('answer')])
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
