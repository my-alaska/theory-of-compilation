import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = [
             'ID',
             'INTNUM',
             'FLOATNUM',
             'STRING',
             'DOTADD',
             'DOTSUB',
             'DOTMUL',
             'DOTDIV',
             'ELESS',
             'EGREATER',
             'EQUALS',
             'NEQUALS',
             'ADDASSIGN',
             'SUBASSIGN',
             'MULASSIGN',
             'DIVASSIGN',
         ] + list(reserved.values())

literals = "+-*/()[]{}=<>:',;"


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOATNUM(t):
    r'(\d*\.\d+)([eE](\+|-)?\d+)?'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t



def t_STRING(t):
    r'\".*?"'
    t.value = str(t.value)
    return t


t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ELESS = r'<='
t_EGREATER = r'>='
t_EQUALS = r'=='
t_NEQUALS = r'!='

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("%d: Illegal character '%s'!" % (t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)


t_ignore_COMMENT = r'\#.*'
t_ignore = '  \t'

lexer = lex.lex()
