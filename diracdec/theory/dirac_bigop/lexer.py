
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

    # '0K'         : 'ZEROK',
    'KET'        : 'KET',
    'ADJK'       : 'ADJK',
    'SCRK'       : 'SCRK',      # infix binary
    'ADDK'       : 'ADDK',      # infix binary
    'MLTK'       : 'MLTK',      # infix binary
    'TSRK'       : 'TSRK',      # infix binary

    # '0B'         : 'ZEROB',
    'BRA'        : 'BRA',
    'ADJB'       : 'ADJB',
    'SCRB'       : 'SCRB',      # infix binary
    'ADDB'       : 'ADDB',      # infix binary
    'MLTB'       : 'MLTB',      # infix binary
    'TSRB'       : 'TSRB',      # infix binary

    # '0O'         : 'ZEROO',
    # '1O'         : 'ONEO', 
    'OUTER'      : 'OUTER',     # infix binary
    'ADJO'       : 'ADJO',
    'SCRO'       : 'SCRO',      # infix binary
    'ADDO'       : 'ADDO',      # infix binary
    'MLTO'       : 'MLTO',      # infix binary
    'TSRO'       : 'TSRO',      # infix binary


    ########################################
    # transpose
    'TRANK'     : 'TRANK',
    'TRANB'     : 'TRANB',
    'TRANO'     : 'TRANO',

    ########################################
    # big-op
    'SUMS'      : 'SUMS',

    ########################################
    # abstraction and application
    'FUN'    : 'LAMBDA',
    
}

tokens = [
    # 'INT', 
    'ID',
    'ZEROK',
    'ZEROB',
    'ZEROO',
    'ONEO',

    # escape to complex scalar
    'COMPLEXSCALAR_EXPR',

    # escape to atomic base
    'ATOMICBASE_EXPR',

    ] + list(reserved.values())

literals = ['(', ')', ',', '.', '@']

t_ZEROK = '0K'
t_ZEROB = '0B'
t_ZEROO = '0O'
t_ONEO = '1O'


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
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