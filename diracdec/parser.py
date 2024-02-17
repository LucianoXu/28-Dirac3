

import ply.yacc as yacc


from .lexer import *

from .theory.trs import *
from .theory.dirac_syntax import *

from .components import py_cscalar
from .components import str_abase, wolfram_abase

precedence = (
)

def p_term(p):
    '''
    trs-term    : trs-var
                | diracbase
                | diracscalar
    '''
    p[0] = p[1]


def p_term_parentheses(p):
    '''
    trs-term    : '(' trs-term ')'
    '''
    p[0] = p[2]

def p_trs_var(p):
    '''
    trs-var     : ID
    '''
    p[0] = TRSVar(p[1])

def p_diracbase(p):
    '''
    diracbase : diracbase-atom
              | diracbase-pair
              | diracbase-fst
              | diracbase-snd
    '''
    p[0] = p[1]

def p_diracbase_atom(p):
    '''
    diracbase-atom : ATOMICBASE_EXPR
    '''
    p[0] = BaseAtom(wolfram_abase.WolframABase(p[1]))

def p_diracbase_pair(p):
    '''
    diracbase-pair : '(' trs-term ',' trs-term ')'
    '''
    p[0] = BasePair(p[2], p[4])

def p_diracbase_fst(p):
    '''
    diracbase-fst : FST '(' trs-term ')'
    '''
    p[0] = BaseFst(p[3])

def p_diracbase_snd(p):
    '''
    diracbase-snd : SND '(' trs-term ')'
    '''
    p[0] = BaseSnd(p[3])


def p_diracscalar(p):
    '''
    diracscalar : diracscalar-c
                | diracscalar-delta
                | diracscalar-add
                | diracscalar-mlt
                | diracscalar-conj
    '''
    p[0] = p[1]

def p_diracscalar_c(p):
    '''
    diracscalar-c : COMPLEXSCALAR_EXPR
    '''
    p[0] = ScalarC(py_cscalar.PyCScalar(complex(p[1])))

def p_diracscalar_delta(p):
    '''
    diracscalar-delta   : DELTA '(' trs-term ',' trs-term ')'
    '''
    p[0] = ScalarDelta(p[3], p[5])

def p_diracscalar_add(p):
    '''
    diracscalar-add     : trs-term ADDS trs-term
    '''
    p[0] = ScalarAdd((p[1], p[3]))

def p_diracscalar_mlt(p):
    '''
    diracscalar-mlt     : trs-term MLTS trs-term
    '''
    p[0] = ScalarMlt((p[1], p[3]))

def p_diracscalar_conj(p):
    '''
    diracscalar-conj    : trs-term CONJS
    '''
    p[0] = ScalarConj(p[1])


def p_error(p):
    if p is None:
        raise RuntimeError("Syntax error: unexpected end of file.")
    raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")

# Build the lexer
parser = yacc.yacc()

def parse(s: str) -> TRSTerm:
    return parser.parse(s)