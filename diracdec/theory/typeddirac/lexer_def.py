
from ply import lex

reserved = {
    'S' : 'S',
    'K' : 'K',
    'B' : 'B',
    'O' : 'O',

    'PAIR'  : 'PAIR',
    'FST'   : 'FST',
    'SND'   : 'SND',

    'DELTA' : 'DELTA',

    'ADJ'   : 'ADJ',
}

tokens = [
    'ID',
    '0S', '0K', '0B', '0O',
    '1S', '1O'
    ] + list(reserved.values())

t_0S = r'0S'
t_0K = r'0K'
t_0B = r'0B'
t_0O = r'0O'
t_1S = r'1S'
t_1O = r'1O'


literals = [
    '(', ')', ',',
    '^', # product
    '|', '>', '<', 
    '*', # scalar multiplication
    '.', # scaling
    '+', 
    '@', # dot
    '&', # tensor product

    ':', # for typing
]


def t_ID(t):
    r'[a-zA-Z\_][a-zA-Z0-9\_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# use // or /* */ to comment
def t_COMMENT(t):
    r'(/\*(.|[\r\n])*?\*/)|(//.*)'
    for c in t.value:
        if c == '\n' or c == '\r\n':
            t.lexer.lineno += 1


# Define a rule so we can track line numbers
def t_newline(t):
    r'[\r\n]+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}'")
