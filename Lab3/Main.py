import os
import re

TOKENS_TYPE = [
    'KEYWORD', 'IDENTIFIER', 'INTEGER_LITERAL',
    'OPERATOR', 'STRING_LITERAL', 'SEPARATOR', 'FLOAT_LITERAL', 'DATA_TYPE', 'BOOL_LITERAL', 'RELATIONAL'
]

TOKENS_DEFINED = {
    '=': 'ASSIGN',
    '+': 'PLUS',
    '++': 'INCREMENT',
    '-': 'MINUS',
    '--': 'DECREMENT',
    '*': 'MUL',
    '/': 'DIV',
    '%': 'MOD',
    '<': 'LT',
    '>': 'GT',
    '>=': 'GET',
    '<=': 'LET',
    '==': 'EQUALITY',
    '!=': 'NOT_EQ',
    '(': 'LR_BRACKET',
    ')': 'RR_BRACKET',
    '{': 'LC_BRACKET',
    '}': 'RC_BRACKET',
    '[': 'LQ_BRACKET',
    ']': 'RQ_BRACKET',
    ',': 'COMMA',
    '"': 'DOUBLE_QUOTE',
    '#': 'COMMENT',
    ';': 'SEMICOLON',
    '!': 'NOT',
    '&&': 'AND',
    '||': 'OR',
    ':': 'COLON'
}

KEYWORD = ["if", "else", "while", "for", "print", "scan", "return", "switch", "case", "break", "fun", "goto", "default"]
SEPARATOR = ['(', ')', '{', '}', '[', ']', ',', '=']
OPERATOR = ['-', '+', '*', '/', '%']
INCR_DECR = ['++', '--']
DATA_TYPE = ['int', 'float', 'string', 'bool', 'void']
RELATIONAL = ['<', '>', '<=', '>=', '!=', '==']
SINGL_REL_OP = ['<', '>']
DOUB_REL_OP = ['<=', '>=', '!=', '==']
PUNCT = [';', ':']
COMMENT = ['#']
ASSIGN_OP = ['=']
BOOL_VAL = ['True', 'False']
LOG_OP = ['||', '&&']
SING_LOG_OP = ['!']


class Element:
    def __init__(self, expr, line_numbers, type):
        self.data = {
            "EXPRESSION": expr,
            "LINE": line_numbers,
            "TYPE": type
        }
        self.next = None


class Token:

    def __init__(self, pos, expr, linenumber):

        if (pos == 10):
            self.type = TOKENS_DEFINED[expr]
        else:
            self.type = TOKENS_TYPE[pos]
        self.expr = expr
        self.line_number = linenumber


class Tokens:

    def __init__(self):
        self.start = None

    def append(self, expr, line_numbers, type):

        new_elem = Element(expr, line_numbers, type)

        if self.start is None:
            self.start = new_elem
            return

        last = self.start

        while (last.next):
            last = last.next
        last.next = new_elem

    def printTok(self):
        temp = self.start
        while (temp):
            print(temp.data)
            temp = temp.next


class Lexer:

    def __init__(self):
        self.tokens = []
        self.count = 1
        self.temp = ''

    def check(self):

        if (self.temp != ''):
            i = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', self.temp)

            if (self.temp in i):

                self.tokens.append(Token(1, self.temp, self.count))
                self.temp = ''

            else:
                print(f"INVALID IDENTIFIER IN LINE: {self.count} ERROR-> {self.temp} ")
                exit()
            self.temp = ''

        else:
            return 0;

    def main(self):

        i = 0

        while i < len(code):

            if (code[i] == ' '):
                self.check()
                i = i + 1
                continue

            if code[i] == '\n':
                self.check()
                self.count = self.count + 1
                i = i + 1
                continue

            elif code[i:i + 2] in DOUB_REL_OP:
                self.check()
                self.tokens.append(Token(9, code[i:i + 2], self.count))
                i = i + 1

            elif code[i:i + 2] in INCR_DECR:
                self.check()
                self.tokens.append(Token(10, code[i:i + 2], self.count))
                i = i + 1

            elif code[i:i + 2] in LOG_OP:
                self.check()
                self.tokens.append(Token(10, code[i:i + 2], self.count))
                i = i + 1

            elif code[i] in COMMENT:
                self.check()
                self.tokens.append(Token(10, code[i], self.count))

            elif code[i] in SEPARATOR:
                self.check()
                self.tokens.append(Token(5, code[i], self.count))

            elif code[i] in PUNCT:
                self.check()
                self.tokens.append(Token(10, code[i], self.count))

            elif code[i] in SINGL_REL_OP:
                self.check()
                self.tokens.append(Token(9, code[i], self.count))

            elif code[i] in ASSIGN_OP:
                self.check()
                self.tokens.append(Token(10, code[i], self.count))

            elif code[i] in SING_LOG_OP:
                self.check()
                self.tokens.append(Token(10, code[i], self.count))

            else:
                self.temp = self.temp + code[i]

                if (code[i] == '"'):
                    # self.tokens.append(Token(4, code[i], self.count))
                    if (self.temp == '"'):
                        self.temp = ''
                        i = i + 1

                        while i < len(code) and code[i] != '"':

                            if (code[i:i + 2] == "\\t"):
                                self.temp = self.temp + '\t'
                                i = i + 2

                            elif (code[i:i + 2] == "\\n"):
                                self.temp = self.temp + '\n'
                                i = i + 2

                            else:
                                self.temp = self.temp + code[i]
                                i = i + 1

                            if (i == len(code) or i > len(code)):
                                print(f"STRING QUOTES ARE NOT CLOSED IN LINE: {self.count} ERROR-> {self.temp} ")
                                exit()

                        if (len(self.temp) > 0):
                            self.tokens.append(Token(4, self.temp, self.count))
                            self.temp = ''
                            i = i + 1
                        continue

                if (self.temp in integer):

                    if (code[i + 1] != '.' and code[i + 1] not in re.findall('[0-9]', code)):

                        j = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', code[i + 1]);

                        if (code[i + 1] not in j):
                            self.tokens.append(Token(2, self.temp, self.count))
                            self.temp = ''

                elif (self.temp in KEYWORD):
                    self.tokens.append(Token(0, self.temp, self.count))
                    self.temp = ''

                elif (self.temp in OPERATOR):
                    self.tokens.append(Token(3, self.temp, self.count))
                    self.temp = ''

                elif (self.temp in DATA_TYPE):
                    self.tokens.append(Token(7, self.temp, self.count))
                    self.temp = ''

                elif (self.temp in BOOL_VAL):
                    self.tokens.append(Token(8, self.temp, self.count))
                    self.temp = ''

                elif (self.temp in RELATIONAL):
                    self.tokens.append(Token(9, self.temp, self.count))
                    self.temp = ''

                elif (self.temp in float):
                    self.tokens.append(Token(6, self.temp, self.count))
                    self.temp = ''

            i = i + 1


def lexer():
    lexer = Lexer()
    lexer.main()
    tok = Tokens()

    for token in lexer.tokens:
        tok.append(token.expr, token.line_number, token.type)
    tok.printTok()


if __name__ == '__main__':

    file_path = r"C:\Users\Adam\PycharmProjects\LFPC\Lab3\test.txt"

    if os.path.isfile(file_path):
        text_file = open(file_path, "r")
        code = text_file.read()
        text_file.close()

integer = re.findall('^[0-9]+$|[0-9]+', code)
float = re.findall(r'[0-9]+\.[0-9]+', code)
print("INPUT:\n", code)
print("OUTPUT:\n")
lexer()