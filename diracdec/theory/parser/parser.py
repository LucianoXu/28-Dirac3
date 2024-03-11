

import ply.yacc as yacc

from typing import Type

from ..dirac.syntax import *
from ..dirac_bigop.syntax import *
from ..dirac_labelled.syntax import *

from .lexer import *

from ..atomic_base import AtomicBase
from ..complex_scalar import ComplexScalar

def construct_parser(CScalar: Type[ComplexScalar], ABase: Type[AtomicBase]) -> yacc.LRParser:

    precedence = (
    )

    def p_trs_item(p):
        '''
        trs-item    : trs-term
                    | subst
        '''
        p[0] = p[1]

    def p_term(p):
        '''
        trs-term    : trs-var
                    | diracbase
                    | diracscalar
                    | diracnotation
                    | set
                    | qreg
                    | qregset
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


    def p_diracbase1(p):
        '''
        diracbase   : ATOMICBASE_EXPR
        '''
        p[0] = ABase(p[1])

    def p_diracbase2(p):
        '''
        diracbase   : PAIR '(' trs-term ',' trs-term ')'
        '''
        p[0] = BasePair(p[3], p[5])

    def p_diracbase3(p):
        '''
        diracbase   : FST '(' trs-term ')'
        '''
        p[0] = BaseFst(p[3])

    def p_diracbase4(p):
        '''
        diracbase   : SND '(' trs-term ')'
        '''
        p[0] = BaseSnd(p[3])


    def p_diracscalar1(p):
        '''
        diracscalar : COMPLEXSCALAR_EXPR
        '''
        p[0] = CScalar(p[1])

    def p_diracscalar2(p):
        '''
        diracscalar : DELTA '(' trs-term ',' trs-term ')'
        '''
        p[0] = ScalarDelta(p[3], p[5])

    def p_diracscalar3(p):
        '''
        diracscalar : trs-term ADDS trs-term
        '''
        p[0] = ScalarAdd(p[1], p[3])

    def p_diracscalar4(p):
        '''
        diracscalar : trs-term MLTS trs-term
        '''
        p[0] = ScalarMlt(p[1], p[3])

    def p_diracscalar5(p):
        '''
        diracscalar : CONJS '(' trs-term ')'
        '''
        p[0] = ScalarConj(p[3])

    def p_diracscalar6(p):
        '''
        diracscalar : trs-term DOT trs-term
        '''
        p[0] = ScalarDot(p[1], p[3])


    # unified symbols
        
    def p_dirac_zero(p):
        '''
        diracnotation    : ZEROX
        '''
        p[0] = Zero()

    def p_dirac_adj(p):
        '''
        diracnotation    : ADJ '(' trs-term ')'
        '''
        p[0] = Adj(p[3])

    def p_dirac_scal(p):
        '''
        diracnotation    : trs-term SCR trs-term
        '''
        p[0] = Scal(p[1], p[3])

    def p_dirac_add(p):
        '''
        diracnotation    : trs-term ADD trs-term
        '''
        p[0] = Add(p[1], p[3])


    # ket
    def p_diracket1(p):
        '''
        diracnotation    : KET '(' trs-term ')'
        '''
        p[0] = KetBase(p[3])


    def p_diracket2(p):
        '''
        diracnotation    : trs-term MLTK trs-term
        '''
        p[0] = KetApply(p[1], p[3])

    def p_diracket3(p):
        '''
        diracnotation    : trs-term TSRK trs-term
        '''
        p[0] = KetTensor(p[1], p[3])

    # bra

    def p_diracbra1(p):
        '''
        diracnotation    : BRA '(' trs-term ')'
        '''
        p[0] = BraBase(p[3])

    def p_diracbra2(p):
        '''
        diracnotation    : trs-term MLTB trs-term
        '''
        p[0] = BraApply(p[1], p[3])

    def p_diracbra3(p):
        '''
        diracnotation    : trs-term TSRB trs-term
        '''
        p[0] = BraTensor(p[1], p[3])


    # operator

    def p_diracop1(p):
        '''
        diracnotation     : ONEO
        '''
        p[0] = OpOne()

    def p_diracop2(p):
        '''
        diracnotation     : trs-term OUTER trs-term
        '''
        p[0] = OpOuter(p[1], p[3])

    def p_diracop3(p):
        '''
        diracnotation     : trs-term MLTO trs-term
        '''
        p[0] = OpApply(p[1], p[3])

    def p_diracop4(p):
        '''
        diracnotation     : trs-term TSRO trs-term
        '''
        p[0] = OpTensor(p[1], p[3])




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
            p[1][p[2].name] = p[4]
            p[0] = p[1]


    
    def p_error(p):
        if p is None:
            raise RuntimeError("Syntax error: unexpected end of file.")
        raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")

    # Build the lexer
    parser = yacc.yacc()

    return parser


