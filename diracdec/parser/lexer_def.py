

from ..theory.dirac import lexer_def as dirac_lex

from ..theory.dirac.lexer_def import *

reserved = {

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

    ########################################
    # qregister
    'PAIRR'     : 'PAIRR',
    'FSTR'      : 'FSTR',
    'SNDR'      : 'SNDR',

    ########################################
    # qreg set
    'ESETR'     : 'ESETR',
    'SETR'      : 'SETR',
    'UNIONR'    : 'UNIONR',
    'SUBR'      : 'SUBR',

    ########################################
    # labeleld Dirac
    'DOTL'      : 'DOTL',
    'MLTKL'     : 'MLTKL',
    'TSRKL'     : 'TSRKL',
    'MLTBL'     : 'MLTBL',
    'TSRBL'     : 'TSRBL',
    'MLTOL'     : 'MLTOL',
    'TSROL'     : 'TSROL',
    'OUTERL'    : 'OUTERL',
}

tokens = [] + list(reserved.values()) + dirac_lex.tokens
reserved.update(dirac_lex.reserved)


literals = ['(', ')', ',', '{', '}', ';' , ':', '.', '@', '[', ']'] + dirac_lex.literals


# t_ID must be redesigned because reserved key words rely on it
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