

from diracdec.parser import lexer_def as dirac_syntax_lexer

from diracdec.parser.lexer_def import *

reserved = {
    'abort'     : 'ABORT',
    'skip'      : 'SKIP',
    'if'        : 'IF',
    'then'      : 'THEN',
    'else'      : 'ELSE',
    'end'       : 'END',
    'while'     : 'WHILE',
    'do'        : 'DO',

    # special program for qwhile-configuration
    'HALT'      : 'HALT'
}

tokens = ['ASSIGN0', 'NUMBER'] + list(reserved.values()) + dirac_syntax_lexer.tokens
reserved.update(dirac_syntax_lexer.reserved)


literals = [';', '<', '>', ','] + dirac_syntax_lexer.literals

t_ASSIGN0 = r":=0"


# we have to redefine t_ID to update the reserved keywords. This is not elegant and we may need a framework for multi-layered parsing based on PLY.
def t_ID(t):
    r'[a-zA-Z\_][a-zA-Z0-9\_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\[\d+\]'
    t.value = int(t.value[1:-1])
    return t

# use // or /* */ to comment
def t_COMMENT(t):
    r'(/\*(.|[\r\n])*?\*/)|(//.*)'
    for c in t.value:
        if c == '\n' or c == '\r\n':
            t.lexer.lineno += 1

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}'")