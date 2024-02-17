
from ply import lex

reserved = {
    'fst'        : 'FST',
    'snd'        : 'SND',
}

tokens = [
    # 'INT', 
    'ID', 
    'ADDS',
    'MLTS',
    'CONJS',
    # 'ZERO',
    # 'ONE',
    'DELTA',
    # 'KET_PARENTHESES',
    # 'BRA_PARENTHESES',
    # 'CDOT',
    # 'OTIMES', 
    'COMPLEXSCALAR_EXPR',
    'ATOMICBASE_EXPR',
    ] + list(reserved.values())

literals = ['(', ')', ',', '+']

t_DELTA = r'δ|\\delta'
t_ADDS = r'\\ADDS'
t_MLTS = r'\\MLTS'
t_CONJS = r'\^\*'

def t_ID(t):
    r'[a-zA-Z\_][a-zA-Z0-9\_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMPLEXSCALAR_EXPR(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_ATOMICBASE_EXPR(t):
    r"'[^']*'"
    t.value = t.value[1:-1]
    return t

# use // or /* */ to comment
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    for c in t.value:
        if c == '\n':
            t.lexer.lineno += 1


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}'")
    


# Build the lexer
lexer = lex.lex()