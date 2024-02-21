

import ply.yacc as yacc

from typing import Type

from .syntax import *

from .lexer import *

def construct_parser(CScalar: Type[ComplexScalar], ABase: Type[AtomicBase]) -> yacc.LRParser:

    precedence = (
    )

    def p_term(p):
        '''
        trs-term    : trs-var
                    | diracbase
                    | diracscalar
                    | diracket
                    | diracbra
                    | diracop
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
        p[0] = BaseAtom(ABase(p[1]))

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
        p[0] = ScalarC(CScalar(p[1]))

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



    def p_diracket1(p):
        '''
        diracket    : ZEROK
        '''
        p[0] = KetZero()


    def p_diracket2(p):
        '''
        diracket    : KET '(' trs-term ')'
        '''
        p[0] = KetBase(p[3])

    def p_diracket3(p):
        '''
        diracket    : ADJK '(' trs-term ')'
        '''
        p[0] = KetAdj(p[3])

    def p_diracket4(p):
        '''
        diracket    : trs-term SCRK trs-term
        '''
        p[0] = KetScal(p[1], p[3])

    def p_diracket5(p):
        '''
        diracket    : trs-term ADDK trs-term
        '''
        p[0] = KetAdd(p[1], p[3])

    def p_diracket6(p):
        '''
        diracket    : trs-term MLTK trs-term
        '''
        p[0] = KetApply(p[1], p[3])

    def p_diracket7(p):
        '''
        diracket    : trs-term TSRK trs-term
        '''
        p[0] = KetTensor(p[1], p[3])


    def p_diracbra1(p):
        '''
        diracbra    : ZEROB
        '''
        p[0] = BraZero()

    def p_diracbra2(p):
        '''
        diracbra    : BRA '(' trs-term ')'
        '''
        p[0] = BraBase(p[3])

    def p_diracbra3(p):
        '''
        diracbra    : ADJB '(' trs-term ')'
        '''
        p[0] = BraAdj(p[3])

    def p_diracbra4(p):
        '''
        diracbra    : trs-term SCRB trs-term
        '''
        p[0] = BraScal(p[1], p[3])

    def p_diracbra5(p):
        '''
        diracbra    : trs-term ADDB trs-term
        '''
        p[0] = BraAdd(p[1], p[3])

    def p_diracbra6(p):
        '''
        diracbra    : trs-term MLTB trs-term
        '''
        p[0] = BraApply(p[1], p[3])

    def p_diracbra7(p):
        '''
        diracbra    : trs-term TSRB trs-term
        '''
        p[0] = BraTensor(p[1], p[3])

    def p_diracop1(p):
        '''
        diracop     : ZEROO
        '''
        p[0] = OpZero()

    def p_diracop2(p):
        '''
        diracop     : ONEO
        '''
        p[0] = OpOne()

    def p_diracop3(p):
        '''
        diracop     : trs-term OUTER trs-term
        '''
        p[0] = OpOuter(p[1], p[3])

    def p_diracop4(p):
        '''
        diracop     : ADJO '(' trs-term ')'
        '''
        p[0] = OpAdj(p[3])

    def p_diracop5(p):
        '''
        diracop     : trs-term SCRO trs-term
        '''
        p[0] = OpScal(p[1], p[3])

    def p_diracop6(p):
        '''
        diracop     : trs-term ADDO trs-term
        '''
        p[0] = OpAdd(p[1], p[3])

    def p_diracop7(p):
        '''
        diracop     : trs-term MLTO trs-term
        '''
        p[0] = OpApply(p[1], p[3])

    def p_diracop8(p):
        '''
        diracop     : trs-term TSRO trs-term
        '''
        p[0] = OpTensor(p[1], p[3])




    def p_error(p):
        if p is None:
            raise RuntimeError("Syntax error: unexpected end of file.")
        raise RuntimeError("Syntax error in input: '" + str(p.value) + "'.")

    # Build the lexer
    parser = yacc.yacc()

    return parser


