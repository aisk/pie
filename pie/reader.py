import re
import cStringIO as StringIO
from pie.scm_type import Symbol

'''Simple scheme reader based on norvig's lispy'''

class Reader(object):
    def __init__(self, file_or_string):
        if not isinstance(file_or_string, file):
            self.file = StringIO.StringIO(file_or_string)
        else:
            self.file = file_or_string
        self.line = ''
    def get_token(self):
        tokenizer = re.compile(
                r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)"""
            )
        while True:
            if self.line == '':
                self.line = self.file.readline()
            if self.line == "":
                return 'EOF'
            token, self.line = tokenizer.match(self.line).groups()
            if token != '' and not token.startswith(';'):
                return token
    def read(self):
        def read_ahead(token):
            if '(' == token:
                l = []
                while True:
                    token = self.get_token()
                    if token == ')':
                        return l
                    else:
                        l.append(read_ahead(token))
            elif ')' == token:
                raise SyntaxError('unexpected )')
            # TODO: add quotes
            elif token == 'EOF':
                raise SyntaxError('unexpected EOF in list')
            else:
                return self.atom(token)
        token1 = self.get_token()
        return 'EOF' if token1 == 'EOF' else read_ahead(token1)

    def atom(self, token):  # TODO
        if token == '#t':
            return True
        elif token == '#f':
            return False
        elif token[0] == '"':
            return token[1:-1].decode('string_escape')
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return Symbol(token)

