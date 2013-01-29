import marshal
import struct
import time
import imp
import opcode
import types

from pie.type import *

code = types.CodeType

def pack_h(value):
    return struct.pack('H', value)
def pack_b(value):
    return struct.pack('B', value)
def pack_l(value):
    return struct.pack('L', value)

class Compiler(object):
    def __init__(self):
        self.consts = []
        self.names = []
        self.varnames = []
        self.codes = []
        self.code_length = 0

        self.LOAD_CONST(self.make_const(None))   # default return value

    def __getattr__(self, name):
        if name not in opcode.opmap:
            return self.__getattribute__(name)
        def opfunc(*args):
            if opcode.opname.index(name) > opcode.HAVE_ARGUMENT:
                if len(args) < 1: raise ValueError('no enough argument')
                self.codes.append(pack_b(opcode.opmap[name]))
                self.codes.append(pack_h(args[0]))
                self.code_length += 3
            else:
                self.codes.append(pack_b(opcode.opmap[name]))
                self.code_length += 1
        return opfunc

    def make_const(self, value):
        self.consts.append(value)
        return len(self.consts) - 1

    def make_name(self, value):
        self.names.append(value)
        return len(self.names) - 1

    def make_varname(self, value):
        self.varnames.append(value)
        return len(self.varnames) - 1

    def compile(self, form):
        if type(form) == Symbol:
            self.LOAD_FAST(0)
        elif type(form) != types.ListType:
            self.LOAD_CONST(self.make_const(form))
        elif form[0] is sym_if:
            if len(form) == 3:
                _, test, conseq = form
                self.compile(test)
                self.POP_JUMP_IF_FALSE(0)
                pos = len(self.codes) - 1
                self.compile(conseq)
                self.codes[pos] = pack_h(self.code_length)
            elif len(form) == 4:
                _, test, conseq, alt = form
                self.compile(test)
                self.POP_JUMP_IF_FALSE(0)
                pos_falsejump = len(self.codes) - 1
                self.compile(conseq)
                self.JUMP_ABSOLUTE(0)
                pos_finishjump = len(self.codes) - 1
                self.codes[pos_falsejump] = pack_h(self.code_length)
                self.compile(alt)
                self.codes[pos_finishjump] = pack_h(self.code_length)
            else:
                raise SyntaxError
            pass
        elif form[0] is sym_define:
            _, name, value = form
            self.compile(value)
            self.STORE_FAST(self.make_varname(name))
        elif form[0] is sym_begin:
            for exp in form[1:]:
                self.compile(exp)
        else:
            func = form[0]
            params = form[1:]
            self.LOAD_GLOBAL(self.make_name(func))
            map(lambda x: self.compile(x), params)
            self.CALL_FUNCTION(len(params))


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

def save_pyc(co, filename):
    ''' save the .pyc file to file '''
    magic_string = imp.get_magic()
    time_string = pack_l(int(time.time()))
    f = open(filename, 'wb')
    f.write(magic_string)
    f.write(time_string)
    marshal.dump(co, f)
    f.close()


