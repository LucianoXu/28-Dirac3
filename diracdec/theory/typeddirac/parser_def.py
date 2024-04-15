

from .syntax import *


precedence = (
    ('nonassoc', ':'),
    ('left', '+'),
    ('left', '*'),
    ('left', '.'),
    ('left', '@'),
    ('left', '&'),
    ('left', '^'),
    ('left', 'CADD'),
    ('left', 'CMUL'),
)

start = 'trs-item'

def p_trs_item(p):
    '''
    trs-item    : term
                | subst
    '''
    p[0] = p[1]

def p_var(p):
    '''
    var     : ID
    '''
    p[0] = Var(p[1])

def p_term_0(p):
    '''
    term    : '(' term ')'
    '''
    p[0] = p[2]

def p_term_1(p):
    '''
    term    : var
    '''
    p[0] = p[1]

def p_type_3(p):
    '''
    term    : term '^' term
    '''
    p[0] = ProdType(p[1], p[3])

def p_type_CS(p):
    '''
    term    : CS
    '''
    p[0] = ComplexScalar()

def p_type_4(p):
    '''
    term    : S
    '''
    p[0] = Sca()

def p_type_5(p):
    '''
    term    : K '(' term ')'
    '''
    p[0] = Ket(p[3])

def p_type_6(p):
    '''
    term    : B '(' term ')'
    '''
    p[0] = Bra(p[3])

def p_type_7(p):
    '''
    term    : O '(' term ',' term ')'
    '''
    p[0] = Opt(p[3], p[5])

def p_term_C1(p):
    '''
    term    : C '(' term ')'
    '''
    p[0] = Complex(p[3])

def p_term_C2(p):
    '''
    term    : term CADD term
    '''
    p[0] = CompAdd(p[1], p[3])

def p_term_C3(p):
    '''
    term    : term CMUL term
    '''
    p[0] = CompMul(p[1], p[3])

def p_term_C4(p):
    '''
    term    : C0
    '''
    p[0] = CompZero()

def p_term_C5(p):
    '''
    term    : C1
    '''
    p[0] = CompOne()

def p_term_C6(p):
    '''
    term    : CADJ '(' term ')'
    '''
    p[0] = CompAdj(p[3])


def p_term_B1(p):
    '''
    term    : PAIR '(' term ',' term ')'
    '''
    p[0] = Pair(p[3], p[5])

def p_term_B2(p):
    '''
    term    : FST '(' term ')'
    '''
    p[0] = Fst(p[3])

def p_term_B3(p):
    '''
    term    : SND '(' term ')'
    '''
    p[0] = Snd(p[3])

def p_term_S1(p):
    '''
    term    : DELTA '(' term ',' term ')'
    '''
    p[0] = Delta(p[3], p[5])

def p_term_D1(p):
    '''
    term    : 0S
    '''
    p[0] = ZeroS()

def p_term_D2(p):
    '''
    term    : 0K '(' term ')'
    '''
    p[0] = ZeroK(p[3])

def p_term_D3(p):
    '''
    term    : 0B '(' term ')'
    '''
    p[0] = ZeroB(p[3])

def p_term_D4(p):
    '''
    term    : 0O '(' term ',' term ')'
    '''
    p[0] = ZeroO(p[3], p[5])

def p_term_D5(p):
    '''
    term    : 1S
    '''
    p[0] = OneS()

def p_term_D6(p):
    '''
    term    : 1O '(' term ')'
    '''
    p[0] = OneO(p[3])

def p_term_D7(p):
    '''
    term    : '|' term '>'
    '''
    p[0] = Ket(p[2])

def p_term_D8(p):
    '''
    term    : '<' term '|'
    '''
    p[0] = Bra(p[2])

def p_term_D9(p):
    '''
    term    : ADJ '(' term ')'
    '''
    p[0] = Adj(p[3])

def p_term_D10(p):
    '''
    term    : term '*' term
    '''
    p[0] = Times(p[1], p[3])

def p_term_D11(p):
    '''
    term    : term '.' term
    '''
    p[0] = Scaling(p[1], p[3])

def p_term_D12(p):
    '''
    term    : term '+' term
    '''
    p[0] = Add(p[1], p[3])

def p_term_D13(p):
    '''
    term    : term '@' term
    '''
    p[0] = Dot(p[1], p[3])

def p_term_D14(p):
    '''
    term    : term '&' term
    '''
    p[0] = Tensor(p[1], p[3])


def p_typing(p):
    '''
    term    : term ':' term
    '''
    p[0] = Typing(p[1], p[3])


# substitution
def p_sub(p):
    '''
    subst   : '{' sub-list '}'
    '''
    p[0] = Subst(p[2])

def p_sub_list(p):
    '''
    sub-list    :
                | sub-list var ':' term ';'
    '''
    if len(p) == 1:
        p[0] = {}
    else:
        p[1][p[2]] = p[4]
        p[0] = p[1]

def p_error(p):
    if p is None:
        raise RuntimeError("Syntax error: unexpected end of file.")
    raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")


