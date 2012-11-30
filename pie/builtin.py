import operator

class Symbol(str):
    pass

sym_define = Symbol('define')
sym_lambda = Symbol('lambda')
sym_if = Symbol('if')
sym_set = Symbol('set!')
sym_quote = Symbol('quote')
sym_begin = Symbol('begin')

sym_begin = Symbol('import')

add = sum

sub = lambda *args: reduce(operator.sub, args)

mul = lambda *args: reduce(operator.mul, args)

div = lambda *args: reduce(operator.div, args)
