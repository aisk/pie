import marshal
import struct
import time
import imp
import opcode
import types

from pie.scm_type import Symbol

def f(): return
code = type(f.__code__)
del f

def pack_h(value):
    return struct.pack('H', value)
def pack_b(value):
    return struct.pack('B', value)

class Compiler(object):
    def __init__(self):
        self.consts = []
        self.names = []
        self.varnames = []
        self.codes = []

        self.LOAD_CONST(self.make_const(None))   # default return value

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

    def make_const(self, value):
        self.consts.append(value)
        return len(self.consts) - 1

    def make_name(self, value):
        self.names.append(value)
        return len(self.names) - 1

    def make_varname(self, value):
        self.varnames.append(value)
        return len(self.varnames)

    def compile(self, form):
        if type(form) == Symbol:
            pass    # TODO: variable
        elif type(form) != types.ListType:
            self.LOAD_CONST(self.make_const(form))
        #if type(form) == types.IntType:
        #    self.LOAD_CONST(self.make_const(form))
        elif form[0] == 'abs':
            func, param = form
            self.LOAD_GLOBAL(self.make_name(func))
            self.compile(param)
            self.CALL_FUNCTION(1)
            self.RETURN_VALUE()
        elif form[0] == 'define':
            _, name, value = form
            self.LOAD_CONST(self.make_const(value))
            self.STORE_FAST(self.make_varname(name))
            self.LOAD_CONST(self.make_const(None))
            self.RETURN_VALUE()
        else:
            raise SyntaxError


    def dump(self):
        self.RETURN_VALUE()

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
    c.compile(['abs', ['abs', ['abs', -42]]])
    return c.dump()

