import marshal
import struct
import time
import imp
import opcode
import types
from opcode import opmap

def f(): return
code = type(f.__code__)
del f

def pack_h(value):
    return struct.pack('H', value)
def pack_b(value):
    return struct.pack('B', value)

class Compiler(object):
    def __init__(self):
        self.consts = [None, ]
        self.names = []
        self.varnames = []
        self.codes = []

    def __getattr__(self, name):
        if name not in opcode.opmap:
            return self.__getattribute__(name)
        def callable(*args):
            if opcode.opname.index(name) > opcode.HAVE_ARGUMENT:
                if len(args) < 1: raise ValueError('no enough argument')
                self.codes.append(pack_b(opcode.opmap[name]))
                self.codes.append(pack_h(args[0]))
            else:
                self.codes.append(pack_b(opcode.opmap[name]))
        return callable

    def add_const(self, value):
        self.consts.append(value)
        return len(self.consts) - 1

    def add_name(self, value):
        self.names.append(value)
        return len(self.names)

    def compile(self, form):
        if type(form) == types.IntType:
            self.consts.append(form)
            return len(self.consts)
        if form[0] == 'abs':
            func, param = form
            self.LOAD_GLOBAL(self.add_name(func))
            self.LOAD_CONST(self.add_const(param))
            self.CALL_FUNCTION(1)
            self.PRINT_ITEM()
            self.PRINT_NEWLINE()
        if form[0] == 'define':
            _, name, value = form
            self.varnames.append(name)
            self.consts.append(value)
            self.LOAD_CONST(len(self.consts) - 1)
            self.STORE_FAST(len(self.varnames) - 1)


    def dump(self):
        self.codes.append(struct.pack('B', opmap['LOAD_CONST']))
        self.consts.append('hahaha')
        self.codes.append(struct.pack('H', len(self.consts) - 1))
        self.codes.append(struct.pack('B', opmap['RETURN_VALUE']))

        code_string = ''.join(self.codes)
        consts = tuple(self.consts)
        names = tuple(self.names)
        varnames = tuple(self.varnames)
        code_args = (
                0,             # 'argcount' arguments count of the code object
                1,             # 'nlocals' ??
                20,            # 'stack_size' max size of the stack
                64,            # 'flags' ??
                code_string,   # 'codestring' the bytecode instructions
                consts,        # 'constants' constants value for the code object
                names,         # 'names' used names in this code object
                varnames,      # 'varnames' variable names
                'test.py',     # 'filename' filename
                '<module>',    # 'name' name of the function/class/module
                1,             # 'firstlineno' the first line number of this code object
                '',            # 'lnotab' ??
                (),            # 'freevars' for closure
                (),            # 'cellvars': ??
            )
        return code(*code_args)


def test_define():
    c = Compiler()
    c.compile(['define', 'a', 1])
    return c.dump()

def test_abs():
    c = Compiler()
    c.compile(['abs', -100])
    return c.dump()

