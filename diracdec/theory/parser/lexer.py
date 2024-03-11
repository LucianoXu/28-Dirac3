
from ply import lex

reserved = {
    'PAIR'       : 'PAIR',
    'FST'        : 'FST',
    'SND'        : 'SND',
    
    # note: the symbol "C" for complex scalars is ommited
    'DELTA'      : 'DELTA',
    'ADDS'       : 'ADDS',      # infix binary
    'MLTS'       : 'MLTS',      # infix binary
    'CONJS'      : 'CONJS',
    'DOT'        : 'DOT',       # infix binary

    # unified symbol
    'ADJ'        : 'ADJ',
    'SCR'        : 'SCR',
    'ADD'        : 'ADD',

    'KET'        : 'KET',
    'MLTK'       : 'MLTK',      # infix binary
    'TSRK'       : 'TSRK',      # infix binary

    'BRA'        : 'BRA',
    'MLTB'       : 'MLTB',      # infix binary
    'TSRB'       : 'TSRB',      # infix binary

    'OUTER'      : 'OUTER',     # infix binary
    'MLTO'       : 'MLTO',      # infix binary
    'TSRO'       : 'TSRO',      # infix binary

    ########################################
    # transpose
    'TP'        : 'TP',

    ########################################
    # for set
    'ESET'      : 'ESET',
    'USET'      : 'USET',
    'UNION'     : 'UNION',

    ########################################
    # big-op
    'SUMS'      : 'SUMS',
    'SUM'       : 'SUM',

    ########################################
    # abstraction and application
    'FUN'       : 'LAMBDA',
}

tokens = [
    # 'INT', 
    'ID',
    'ZEROX',
    'ONEO',

    # escape to complex scalar
    'COMPLEXSCALAR_EXPR',

    # escape to atomic base
    'ATOMICBASE_EXPR',

    ] + list(reserved.values())


literals = ['(', ')', ',', '{', '}', ';' , ':', '.', '@']

t_ZEROX = '0X'
t_ONEO = '1O'


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
    r'[\r\n]+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}'")
    


# Build the lexer
lexer = lex.lex()