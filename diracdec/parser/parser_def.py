
from ..theory.dirac import parser_def as dirac_parser

from ..theory.dirac.syntax import *
from ..theory.dirac_bigop.syntax import *
from ..theory.dirac_labelled.syntax import *



precedence = (
)

from ..theory.dirac.parser_def import p_dirac_add, p_dirac_adj, p_dirac_scal, p_dirac_zero, p_diracbase2, p_diracbase3, p_diracbase4, p_diracbra1, p_diracbra2, p_diracbra3, p_diracket1, p_diracket2, p_diracket3, p_diracop1, p_diracop2, p_diracop3, p_diracop4, p_diracscalar2, p_diracscalar3, p_diracscalar4, p_diracscalar5, p_diracscalar6, p_term, p_term_parentheses, p_trs_item, p_trs_var

start = "trs-item"

def p_term_append(p):
    '''
    trs-term    : set
                | qreg
                | qregset
                | diracnotationL
    '''
    p[0] = p[1]



##############################
# transpose
    
def p_dirac_tp(p):
    '''
    diracnotation    : TP '(' trs-term ')'
    '''
    p[0] = Transpose(p[3])

##############################
# set
def p_set_eset(p):
    '''
    set : ESET
    '''
    p[0] = EmptySet()

def p_set_uset(p):
    '''
    set : USET
    '''
    p[0] = UniversalSet()

def p_set_union(p):
    '''
    set : trs-term UNION trs-term
    '''
    p[0] = UnionSet(p[1], p[3])

##############################
# big-op
    
def p_dirac_sums(p):
    '''
    diracnotation : SUMS '(' trs-var ',' trs-term ',' trs-term ')'
                    | SUMS '(' trs-var ',' trs-term ')'
    '''
    if len(p) == 9:
        p[0] = SumS(((p[3], p[5]),), p[7])
    elif len(p) == 7:
        p[0] = SumS(((p[3], UniversalSet()),), p[5])
    else:
        raise Exception()


def p_dirac_sum(p):
    '''
    diracnotation : SUM '(' trs-var ',' trs-term ',' trs-term ')'
                    | SUM '(' trs-var ',' trs-term ')'
    '''
    if len(p) == 9:
        p[0] = Sum(((p[3], p[5]),), p[7])
    elif len(p) == 7:
        p[0] = Sum(((p[3], UniversalSet()),), p[5])
    else:
        raise Exception()
    

##############################
# abstraction and application
def p_abstract(p):
    '''
    trs-term    : LAMBDA trs-var '.' trs-term
    '''
    p[0] = Abstract(p[2], p[4])

def p_apply(p):
    '''
    trs-term    : trs-term '@' trs-term
    '''
    p[0] = Apply(p[1], p[3])

# substitution
def p_sub(p):
    '''
    subst   : '{' sub-list '}'
    '''
    p[0] = Subst(p[2])

def p_sub_list(p):
    '''
    sub-list    :
                | sub-list trs-var ':' trs-item ';'
    '''
    if len(p) == 1:
        p[0] = {}
    else:
        p[1][p[2]] = p[4]
        p[0] = p[1]


#####################################
# quantum register
    
def p_qreg1(p):
    '''
    qreg    : PAIRR '(' trs-term ',' trs-term ')'
    '''
    p[0] = QRegPair(p[3], p[5])

def p_qreg2(p):
    '''
    qreg   : FSTR '(' trs-term ')'
    '''
    p[0] = QRegFst(p[3])

def p_qreg3(p):
    '''
    qreg   : SNDR '(' trs-term ')'
    '''
    p[0] = QRegSnd(p[3])

#####################################
# qreg set
    
def p_qregset1(p):
    '''
    qregset : ESETR
    '''
    p[0] = EmptyRSet()

def p_qregset2(p):
    '''
    qregset : SETR '(' trs-term ')'
    '''
    p[0] = RegRSet(p[3])

def p_qregset3(p):
    '''
    qregset : trs-term UNIONR trs-term
    '''
    p[0] = UnionRSet(p[1], p[3])

def p_qregset4(p):
    '''
    qregset : trs-term SUBR trs-term
    '''
    p[0] = SubRSet(p[1], p[3])


#########################################
# labelled Dirac notation
def p_diracscalar7(p):
    '''
    diracscalar : trs-term DOTL trs-term
    '''
    p[0] = ScalarDotL(p[1], p[3])

def p_diracnotationL1(p):
    '''
    diracnotationL  : trs-term '[' trs-term ']'
    '''
    p[0] = Labelled1(p[1], p[3])

def p_diracnotationL2(p):
    '''
    diracnotationL  : trs-term '[' trs-term ';' trs-term ']'
    '''
    p[0] = Labelled2(p[1], p[3], p[5])


def p_dirac_ketL1(p):
    '''
    diracnotationL : trs-term MLTKL trs-term
    '''
    p[0] = KetApplyL(p[1], p[3])

def p_dirac_ketL2(p):
    '''
    diracnotationL : trs-term TSRKL trs-term
    '''
    p[0] = KetTensorL(p[1], p[3])

def p_dirac_braL1(p):
    '''
    diracnotationL : trs-term MLTBL trs-term
    '''
    p[0] = BraApplyL(p[1], p[3])

def p_dirac_braL2(p):
    '''
    diracnotationL : trs-term TSRBL trs-term
    '''
    p[0] = BraTensorL(p[1], p[3])

def p_dirac_opL1(p):
    '''
    diracnotationL : trs-term OUTERL trs-term
    '''
    p[0] = OpOuterL(p[1], p[3])

def p_dirac_opL2(p):
    '''
    diracnotationL : trs-term MLTOL trs-term
    '''
    p[0] = OpApplyL(p[1], p[3])

def p_dirac_opL3(p):
    '''
    diracnotationL : trs-term TSROL trs-term
    '''
    p[0] = OpTensorL(p[1], p[3])


def p_error(p):
    if p is None:
        raise RuntimeError("Syntax error: unexpected end of file.")
    raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")