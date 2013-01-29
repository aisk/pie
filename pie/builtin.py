import operator

add = sum

sub = lambda *args: reduce(operator.sub, args)

mul = lambda *args: reduce(operator.mul, args)

div = lambda *args: reduce(operator.div, args)
