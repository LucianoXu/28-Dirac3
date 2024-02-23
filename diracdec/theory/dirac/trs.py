
'''
all the rewriting rules for Dirac notation
'''

from __future__ import annotations
import datetime

from typing import Type

from ply import yacc

from ..trs import *
from .syntax import *
from ..atomic_base import AtomicBase
from ..complex_scalar import ComplexScalar

from .parser import construct_parser

def construct_trs(
        CScalar: Type[ComplexScalar], 
        ABase: Type[AtomicBase], 
        parser: yacc.LRParser|None = None) -> TRS:

    # construct the parser
    if parser is None:
        parser = construct_parser(CScalar, ABase)

    def parse(s: str) -> TRSTerm:
        return parser.parse(s)


    # prepare the rules
    rules = []


    C0 = CScalar.zero()
    C1 = CScalar.one()
    C2 = CScalar.add(CScalar.one(), CScalar.one())

    
    #################################################
    # reducing basis and complex scalars

    def atomic_base_rewrite(rule, term, side_info):
        if isinstance(term, ABase):
            return term.reduce()
    ATOMIC_BASE = TRSRule(
        lhs = "a",
        rhs = "a",
        rewrite_method=atomic_base_rewrite,
        rule_repr="(* base -> simp(base) *)"
    )
    rules.append(ATOMIC_BASE)

    def complex_scalar_rewrite(rule, term, side_info):
        if isinstance(term, CScalar):
            return term.reduce()
    COMPLEX_SCALAR = TRSRule(
        lhs = "a",
        rhs = "a",
        rewrite_method=complex_scalar_rewrite,
        rule_repr="(* complex -> simp(complex) *)"
    )
    rules.append(COMPLEX_SCALAR)


    #################################################
    # Base
    BASIS_1 = TRSRule(
        lhs = parse("FST(PAIR(s, t))"),
        rhs = parse("s")
    )
    rules.append(BASIS_1)

    BASIS_2 = TRSRule(
        lhs = parse("SND(PAIR(s, t))"),
        rhs = parse("t")
    )
    rules.append(BASIS_2)

    BASIS_3 = TRSRule(
        lhs = parse("PAIR(FST(s), SND(s))"),
        rhs = parse("s")
    )
    rules.append(BASIS_3)

    #################################################
    # Delta
    def delta_1_rewrite(rule, term, side_info):
        if isinstance(term, ScalarDelta):
            if isinstance(term.args[0], BasePair):
                return ScalarMlt(
                    ScalarDelta(term.args[0].args[0], BaseFst(term.args[1])),
                    ScalarDelta(term.args[0].args[1], BaseSnd(term.args[1]))
                    )
            if isinstance(term.args[1], BasePair):
                return ScalarMlt(
                    ScalarDelta(BaseFst(term.args[0]), term.args[1].args[0]),
                    ScalarDelta(BaseSnd(term.args[0]), term.args[1].args[1])
                    )
    DELTA_1 = TRSRule(
        lhs = "DELTA(s, PAIR(t1, t2))",
        rhs = "DELTA(FST(s), t1) MLTS DELTA(SND(s), t2)",
        rewrite_method=delta_1_rewrite
    )
    rules.append(DELTA_1)


    def delta_2_rewrite(rule, term, side_info):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ScalarDelta) \
                    and isinstance(term.args[i].args[0], BaseFst) \
                    and isinstance(term.args[i].args[1], BaseFst):
                    for j in range(len(term.args)):
                        if i == j:
                            continue
                        if isinstance(term.args[j], ScalarDelta) \
                            and isinstance(term.args[j].args[0], BaseSnd) \
                            and isinstance(term.args[j].args[1], BaseSnd):

                            deltauv = ScalarDelta(term.args[i].args[0].args[0], term.args[j].args[0].args[0])

                            return ScalarMlt(deltauv, *term.remained_terms(i, j))
    DELTA_2 = TRSRule(
        lhs = "DELTA(FST(s), FST(t)) MLTS DELTA(SND(s), SND(t))",
        rhs = "DELTA(s, t)",
        rewrite_method=delta_2_rewrite
    )
    rules.append(DELTA_2)


    #################################################
    # Scalar

    def scr_complex_1_rewrite(rule, term, side_info):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                if term.args[i] == C0:
                    return ScalarAdd(*term.remained_terms(i))

    SCR_COMPLEX_1 = TRSRule(
        lhs="C(0) ADDS a", 
        rhs="a",
        rewrite_method=scr_complex_1_rewrite
    )
    rules.append(SCR_COMPLEX_1)


    def scr_complex_2_rewrite(rule, term, side_info):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ComplexScalar):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], ComplexScalar):

                            new_args = (CScalar.add(term.args[i], term.args[j]),) + term.remained_terms(i, j)

                            return ScalarAdd(*new_args)

    SCR_COMPLEX_2 = TRSRule(
        lhs="C(a) ADDS C(b)", 
        rhs="C(a + b)",
        rewrite_method=scr_complex_2_rewrite
    )
    rules.append(SCR_COMPLEX_2)

    def scr_complex_3_rewrite(rule, term, side_info):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                for j in range(i+1, len(term.args)):
                    if term.args[i] == term.args[j]:
                        new_args = (ScalarMlt(C2, term.args[i]),) + term.remained_terms(i, j)
                        return ScalarAdd(*new_args)
                    
    SCR_COMPLEX_3 = TRSRule(
        lhs = "S0 ADDS S0",
        rhs = "C(1 + 1) MLTS S0",
        rewrite_method=scr_complex_3_rewrite
    )
    rules.append(SCR_COMPLEX_3)

    def scr_complex_4_rewrite(rule, term, side_info):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ScalarMlt):
                    for j in range(len(term.args[i].args)):
                        if isinstance(term.args[i].args[j], ComplexScalar):
                            S0 = ScalarMlt(*term.args[i].args[:j], *term.args[i].args[j+1:])
                            for k in range(len(term.args)):
                                if S0 == term.args[k]:
                                    new_args = (ScalarMlt(CScalar.add(term.args[i].args[j], CScalar.one()), term[k]),)
                                    new_args += term.remained_terms(i, k)
                                    return ScalarAdd(*new_args)
                                
    SCR_COMPLEX_4 = TRSRule(
        lhs = "(C(a) MLTS S0) ADDS S0",
        rhs = "C(a + 1) MLTS S0",
        rewrite_method=scr_complex_4_rewrite
    )
    rules.append(SCR_COMPLEX_4)

    def scr_complex_5_rewrite(rule, term, side_info):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ScalarMlt):
                    for j in range(len(term.args[i].args)):
                        if isinstance(term.args[i].args[j], ComplexScalar):
                            S0 = ScalarMlt(*term.args[i].args[:j], *term.args[i].args[j+1:])
                            for k in range(i+1, len(term.args)):
                                if isinstance(term.args[k], ScalarMlt):
                                    for l in range(len(term.args[k].args)):
                                        if isinstance(term.args[k].args[l], ComplexScalar):
                                            S1 = ScalarMlt(*term.args[k].args[:l], *term.args[k].args[l+1:])
                                            if S0 == S1:
                                                new_args = (ScalarMlt(CScalar.add(term.args[i].args[j], term.args[k].args[l]), S0),)
                                                new_args += term.remained_terms(i, k)
                                                return ScalarAdd(*new_args)

    SCR_COMPLEX_5 = TRSRule(
        lhs = "(C(a) MLTS S0) ADDS (C(b) MLTS S0)",
        rhs = "C(a + b) MLTS S0",
        rewrite_method=scr_complex_5_rewrite
    )
    rules.append(SCR_COMPLEX_5)

    def scr_complex_6_rewrite(rule, term, side_info):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if term.args[i] == C0:
                    return C0

    SCR_COMPLEX_6 = TRSRule(
        lhs="C(0) MLTS a", 
        rhs="C(0)",
        rewrite_method=scr_complex_6_rewrite
    )
    rules.append(SCR_COMPLEX_6)

    def scr_complex_7_rewrite(rule, term, side_info):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if term.args[i] == C1:
                    return ScalarMlt(*term.remained_terms(i))
    SCR_COMPLEX_7 = TRSRule(
        lhs="C(1) MLTS a", 
        rhs="a",
        rewrite_method=scr_complex_7_rewrite
    )
    rules.append(SCR_COMPLEX_7)


    def scr_complex_8_rewrite(rule, term, side_info):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ComplexScalar):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], ComplexScalar):

                            new_args = (CScalar.mlt(term.args[i], term.args[j]),) + term.remained_terms(i, j)

                            return ScalarMlt(*new_args)

    SCR_COMPLEX_8 = TRSRule(
        lhs="C(a) MLTS C(b)",
        rhs="C(a * b)",
        rewrite_method=scr_complex_8_rewrite
    )
    rules.append(SCR_COMPLEX_8)

    def scr_complex_9_rewrite(rule, term, side_info):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ScalarAdd):
                    S1 = ScalarMlt(*term.args[:i], *term.args[i+1:])
                    new_args = tuple(ScalarMlt(S1, term.args[i][j]) for j in range(len(term.args[i].args)))
                    return ScalarAdd(*new_args)
    SCR_COMPLEX_9 = TRSRule(
        lhs="a MLTS (b ADDS c)",
        rhs="(a MLTS b) ADDS (a MLTS c)",
        rewrite_method=scr_complex_9_rewrite
    )
    rules.append(SCR_COMPLEX_9)


    def scr_complex_10_rewrite(rule, term, side_info):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ComplexScalar):
                return CScalar.conj(term.args[0])
    SCR_COMPLEX_10 = TRSRule(
        lhs="CONJS(C(a))",
        rhs="C(a ^*)",
        rewrite_method=scr_complex_10_rewrite
    )
    rules.append(SCR_COMPLEX_10)
        

    def scr_complex_11_rewrite(rule, term, side_info):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ScalarDelta):
                return term.args[0]
            
    SCR_COMPLEX_11 = TRSRule(
        lhs="CONJS(DELTA(a, b))",
        rhs="DELTA(a, b)",
        rewrite_method=scr_complex_11_rewrite
    )
    rules.append(SCR_COMPLEX_11)


    def scr_complex_12_rewrite(rule, term, side_info):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ScalarAdd):
                new_args = tuple(ScalarConj(arg) for arg in term.args[0].args)
                return ScalarAdd(*new_args)
    SCR_COMPLEX_12 = TRSRule(
        lhs="CONJS(a ADDS b)",
        rhs="CONJS(a) ADDS CONJS(b)",
        rewrite_method=scr_complex_12_rewrite
    )
    rules.append(SCR_COMPLEX_12)


    def scr_complex_13_rewrite(rule, term, side_info):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ScalarMlt):
                new_args = tuple(ScalarConj(arg) for arg in term.args[0].args)
                return ScalarMlt(*new_args)
    SCR_COMPLEX_13 = TRSRule(
        lhs="CONJS(a MLTS b)",
        rhs="CONJS(a) MLTS CONJS(b)",
        rewrite_method=scr_complex_13_rewrite
    )
    rules.append(SCR_COMPLEX_13)


    SCR_COMPLEX_14 = TRSRule(
        lhs=parse(r''' CONJS(CONJS(a)) '''), 
        rhs=parse(r''' a ''')
    )
    rules.append(SCR_COMPLEX_14)

    SCR_COMPLEX_15 = TRSRule(
        lhs = parse(r''' CONJS(B0 DOT K0) '''),
        rhs = parse(r''' ADJB(K0) DOT ADJK(B0) ''')
    )
    rules.append(SCR_COMPLEX_15)


    SCR_DOT_1 = TRSRule(
        lhs = parse(r''' 0B DOT K0 '''),
        rhs = parse(r''' "0" '''),
        rule_repr = '''0B DOT K0 -> C(0) ;'''
    )
    rules.append(SCR_DOT_1)

    SCR_DOT_2 = TRSRule(
        lhs = parse(r''' B0 DOT 0K '''),
        rhs = parse(r''' "0" '''),
        rule_repr = '''B0 DOT 0K -> C(0) ;'''
    )
    rules.append(SCR_DOT_2)

    SCR_DOT_3 = TRSRule(
        lhs = parse(r'''(S0 SCRB B0) DOT K0'''),
        rhs = parse(r'''S0 MLTS (B0 DOT K0)''')
    )
    rules.append(SCR_DOT_3)


    SCR_DOT_4 = TRSRule(
        lhs = parse(r'''B0 DOT (S0 SCRK K0)'''),
        rhs = parse(r'''S0 MLTS (B0 DOT K0)''')
    )
    rules.append(SCR_DOT_4)

    def scr_dot_5(rule, term, side_info):
        if isinstance(term, ScalarDot):
            if isinstance(term.args[0], BraAdd):
                new_args = tuple(ScalarDot(arg, term.args[1]) for arg in term.args[0].args)
                return ScalarAdd(*new_args)
    SCR_DOT_5 = TRSRule(
        lhs = "(B1 ADDB B2) DOT K0",
        rhs = "(B1 DOT K0) ADDS (B2 DOT K0)",
        rewrite_method=scr_dot_5
    )
    rules.append(SCR_DOT_5)

    def scr_dot_6(rule, term, side_info):
        if isinstance(term, ScalarDot):
            if isinstance(term.args[1], KetAdd):
                new_args = tuple(ScalarDot(term.args[0], arg) for arg in term.args[1].args)
                return ScalarAdd(*new_args)
    SCR_DOT_6 = TRSRule(
        lhs = "B0 DOT (K1 ADDK K2)",
        rhs = "(B0 DOT K1) ADDS (B0 DOT K2)",
        rewrite_method=scr_dot_6
    )
    rules.append(SCR_DOT_6)


    SCR_DOT_7 = TRSRule(
        lhs = parse(r''' (BRA(s) DOT KET(t)) '''),
        rhs = parse(r''' DELTA(s, t) ''')
    )
    rules.append(SCR_DOT_7)


    SCR_DOT_8 = TRSRule(
        lhs = parse(r'''(B1 TSRB B2) DOT KET(t)'''),
        rhs = parse(r'''(B1 DOT KET(FST(t))) MLTS (B2 DOT KET(SND(t)))''')
    )
    rules.append(SCR_DOT_8)

            
    SCR_DOT_9 = TRSRule(
        lhs = parse(r'''BRA(s) DOT (K1 TSRK K2)'''),
        rhs = parse(r'''(BRA(FST(s)) DOT K1) MLTS (BRA(SND(s)) DOT K2)''')
    )
    rules.append(SCR_DOT_9)

            
    SCR_DOT_10 = TRSRule(
        lhs = parse(r'''(B1 TSRB B2) DOT (K1 TSRK K2)'''),
        rhs = parse(r'''(B1 DOT K1) MLTS (B2 DOT K2)'''),
    )
    rules.append(SCR_DOT_10)

    SCR_SORT_1 = TRSRule(
        lhs = parse(r''' (B0 MLTB O0) DOT K0 '''),
        rhs = parse(r''' B0 DOT (O0 MLTK K0) ''')
    )
    rules.append(SCR_SORT_1)

    SCR_SORT_2 = TRSRule(
        lhs = parse(r''' BRA(s) DOT ((O1 TSRO O2) MLTK K0) '''),
        rhs = parse(r''' ((BRA(FST(s)) MLTB O1) TSRB (BRA(SND(s)) MLTB O2)) DOT K0 ''')
    )
    rules.append(SCR_SORT_2)

    SCR_SORT_3 = TRSRule(
        lhs = parse(r''' (B1 TSRB B2) DOT ((O1 TSRO O2) MLTK K0) '''),
        rhs = parse(r''' ((B1 MLTB O1) TSRB (B2 MLTB O2)) DOT K0''')
    )
    rules.append(SCR_SORT_3)




    #######################################
    # Ket

    KET_ADJ_1 = TRSRule(
        lhs = parse(r'''ADJK(0B)'''),
        rhs = parse(r'''0K''')
    )
    rules.append(KET_ADJ_1)

    KET_ADJ_2 = TRSRule(
        lhs = parse(r'''ADJK(BRA(s))'''),
        rhs = parse(r'''KET(s)''')
    )
    rules.append(KET_ADJ_2)

    KET_ADJ_3 = TRSRule(
        lhs = parse(r'''ADJK(ADJB(K0))'''),
        rhs = parse(r'''K0''')
    )
    rules.append(KET_ADJ_3)

    KET_ADJ_4 = TRSRule(
        lhs = parse(r'''ADJK(S0 SCRB B0)'''),
        rhs = parse(r'''CONJS(S0) SCRK ADJK(B0)'''),
    )
    rules.append(KET_ADJ_4)

    def ket_adj_5_rewrite(rule, term, side_info):
        if isinstance(term, KetAdj):
            if isinstance(term.args[0], BraAdd):
                new_args = tuple(KetAdj(arg) for arg in term.args[0].args)
                return KetAdd(*new_args)
    KET_ADJ_5 = TRSRule(
        lhs = "ADJK(B1 ADDB B2)",
        rhs = "ADJK(B1) ADDK ADJK(B2)",
        rewrite_method=ket_adj_5_rewrite
    )
    rules.append(KET_ADJ_5)

    KET_ADJ_6 = TRSRule(
        lhs = parse(r'''ADJK(B0 MLTB O0)'''),
        rhs = parse(r'''ADJO(O0) MLTK ADJK(B0)''')
    )
    rules.append(KET_ADJ_6)

    KET_ADJ_7 = TRSRule(
        lhs = parse(r''' ADJK(B1 TSRB B2) '''),
        rhs = parse(r''' ADJK(B1) TSRK ADJK(B2) ''')
    )
    rules.append(KET_ADJ_7)


    KET_SCAL_1 = TRSRule(
        lhs = parse(r''' "0" SCRK K0 '''),
        rhs = parse(r''' 0K '''),
        rule_repr = '''C(0) SCRK K0 -> 0K ;'''
    )
    rules.append(KET_SCAL_1)


    KET_SCAL_2 = TRSRule(
        lhs = parse(r''' "1" SCRK K0 '''),
        rhs = parse(r''' K0 '''),
        rule_repr = '''C(1) SCRK K0 -> K0 ;'''
    )
    rules.append(KET_SCAL_2)

    KET_SCAL_3 = TRSRule(
        lhs = parse(r'''S0 SCRK 0K'''),
        rhs = parse(r''' 0K ''')
    )
    rules.append(KET_SCAL_3)

        
    KET_SCAL_4 = TRSRule(
        lhs = parse(r'''S1 SCRK (S2 SCRK K0)'''),
        rhs = parse(r'''(S1 MLTS S2) SCRK K0'''),
    )
    rules.append(KET_SCAL_4)


    def ket_scal_5_rewrite(rule, term, side_info):
        if isinstance(term, KetScal):
            if isinstance(term.args[1], KetAdd):
                new_args = tuple(KetScal(term.args[0], arg) for arg in term.args[1].args)
                return KetAdd(*new_args)
            
    KET_SCAL_5 = TRSRule(
        lhs = "S0 SCRK (K1 ADDK K2)",
        rhs = "(S0 SCRK K1) ADDK (S0 SCRK K2)",
        rewrite_method=ket_scal_5_rewrite
    )
    rules.append(KET_SCAL_5)


    def ket_add_1(rule, term, side_info):
        if isinstance(term, KetAdd):
            for i in range(len(term.args)):
                if term.args[i] == KetZero():
                    return KetAdd(*term.remained_terms(i))
    KET_ADD_1 = TRSRule(
        lhs = "0K ADDK K0",
        rhs = "K0",
        rewrite_method=ket_add_1
    )
    rules.append(KET_ADD_1)

    def ket_add_2(rule, term, side_info):
        if isinstance(term, KetAdd):
            for i in range(len(term.args)):
                for j in range(i+1, len(term.args)):
                    if term.args[i] == term.args[j]:
                        new_args = (KetScal(C2, term.args[i]),) + term.remained_terms(i, j)
                        return KetAdd(*new_args)
    KET_ADD_2 = TRSRule(
        lhs = "K0 ADDK K0",
        rhs = "C(1 + 1) SCRK K0",
        rewrite_method=ket_add_2
    )
    rules.append(KET_ADD_2)

    def ket_add_3(rule, term, side_info):
        if isinstance(term, KetAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], KetScal):
                    for j in range(len(term.args)):
                        if term.args[i].args[1] == term.args[j]:
                            new_args = (
                                KetScal(ScalarAdd(term.args[i].args[0], C1), term.args[j]),) + term.remained_terms(i, j)
                            return KetAdd(*new_args)
    KET_ADD_3 = TRSRule(
        lhs = "(S0 SCRK K0) ADDK K0",
        rhs = "(S0 ADDS C(1)) SCRK K0",
        rewrite_method=ket_add_3
    )
    rules.append(KET_ADD_3)

    def ket_add_4(rule, term, side_info):
        if isinstance(term, KetAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], KetScal):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], KetScal):
                            if term.args[i].args[1] == term.args[j].args[1]:
                                new_args = (KetScal(ScalarAdd(term.args[i].args[0], term.args[j].args[0]), term.args[i].args[1]),) + term.remained_terms(i, j)
                                return KetAdd(*new_args)
    KET_ADD_4 = TRSRule(
        lhs = "(S1 SCRK K0) ADDK (S2 SCRK K0)",
        rhs = "(S1 ADDS S2) SCRK K0",
        rewrite_method=ket_add_4
    )
    rules.append(KET_ADD_4)


    KET_MUL_1 = TRSRule(
        lhs = parse(r'''0O MLTK K0'''),
        rhs = parse(r'''0K''')
    )
    rules.append(KET_MUL_1)

    KET_MUL_2 = TRSRule(
        lhs = parse(r'''O0 MLTK 0K'''),
        rhs = parse(r'''0K''')
    )
    rules.append(KET_MUL_2)

    KET_MUL_3 = TRSRule(
        lhs = parse(r'''1O MLTK K0'''),
        rhs = parse(r'''K0''')
    )
    rules.append(KET_MUL_3)

    KET_MUL_4 = TRSRule(
        lhs = parse(r'''(S0 SCRO O0) MLTK K0'''),
        rhs = parse(r'''S0 SCRK (O0 MLTK K0)''')
    )
    rules.append(KET_MUL_4)

    KET_MUL_5 = TRSRule(
        lhs = parse(r'''O0 MLTK (S0 SCRK K0)'''),
        rhs = parse(r'''S0 SCRK (O0 MLTK K0)''')
    )
    rules.append(KET_MUL_5)


    def ket_mul_6_rewrite(rule, term, side_info):
        if isinstance(term, KetApply) and isinstance(term.args[0], OpAdd):
            new_args = tuple(KetApply(arg, term[1]) for arg in term.args[0].args)
            return KetAdd(*new_args)
    KET_MUL_6 = TRSRule(
        lhs = "(O1 ADDO O2) MLTK K0",
        rhs = "(O1 MLTK K0) ADDK (O2 MLTK K0)",
        rewrite_method=ket_mul_6_rewrite
    )
    rules.append(KET_MUL_6)


    def ket_mul_7_rewrite(rule, term, side_info):
        if isinstance(term, KetApply) and isinstance(term.args[1], KetAdd):
            new_args = tuple(KetApply(term[0], arg) for arg in term.args[1].args)
            return KetAdd(*new_args)
    KET_MUL_7 = TRSRule(
        lhs = "O0 MLTK (K1 ADDK K2)",
        rhs = "(O0 MLTK K1) ADDK (O0 MLTK K2)",
        rewrite_method=ket_mul_7_rewrite
    )
    rules.append(KET_MUL_7)

    KET_MUL_8 = TRSRule(
        lhs = parse(r'''(K1 OUTER B0) MLTK K2'''),
        rhs = parse(r'''(B0 DOT K2) SCRK K1''')
    )
    rules.append(KET_MUL_8)

    KET_MUL_9 = TRSRule(
        lhs = parse(r'''(O1 MLTO O2) MLTK K0'''),
        rhs = parse(r'''O1 MLTK (O2 MLTK K0)''')
    )
    rules.append(KET_MUL_9)


    KET_MUL_10 = TRSRule(
        lhs = parse(r'''(O1 TSRO O2) MLTK ((O1_ TSRO O2_) MLTK K0)'''),
        rhs = parse(r'''((O1 MLTO O1_) TSRO (O2 MLTO O2_)) MLTK K0''')
    )
    rules.append(KET_MUL_10)

    KET_MUL_11 = TRSRule(
        lhs = parse(r'''(O1 TSRO O2) MLTK KET(t)'''),
        rhs = parse(r'''(O1 MLTK KET(FST(t))) TSRK (O2 MLTK KET(SND(t)))''')
    )
    rules.append(KET_MUL_11)

    KET_MUL_12 = TRSRule(
        lhs = parse(r'''(O1 TSRO O2) MLTK (K1 TSRK K2)'''),
        rhs = parse(r'''(O1 MLTK K1) TSRK (O2 MLTK K2)''')
    )
    rules.append(KET_MUL_12)

    KET_TSR_1 = TRSRule(
        lhs = parse(r'''0K TSRK K0'''),
        rhs = parse(r'''0K''')
    )
    rules.append(KET_TSR_1)

    KET_TSR_2 = TRSRule(
        lhs = parse(r'''K0 TSRK 0K'''),
        rhs = parse(r'''0K''')
    )
    rules.append(KET_TSR_2)

    KET_TSR_3 = TRSRule(
        lhs = parse(r'''KET(s) TSRK KET(t)'''),
        rhs = parse(r'''KET(PAIR(s, t))''')
    )
    rules.append(KET_TSR_3)

    KET_TSR_4 = TRSRule(
        lhs = parse(r'''(S0 SCRK K1) TSRK K2'''),
        rhs = parse(r'''S0 SCRK (K1 TSRK K2)''')
    )
    rules.append(KET_TSR_4)

    KET_TSR_5 = TRSRule(
        lhs = parse(r'''K1 TSRK (S0 SCRK K2)'''),
        rhs = parse(r'''S0 SCRK (K1 TSRK K2)''')
    )
    rules.append(KET_TSR_5)

    def ket_tsr_6_rewrite(rule, term, side_info):
        if isinstance(term, KetTensor) and isinstance(term.args[0], KetAdd):
            new_args = tuple(KetTensor(arg, term[1]) for arg in term.args[0].args)
            return KetAdd(*new_args)
    KET_TSR_6 = TRSRule(
        lhs = "(K1 ADDK K2) TSRK K0",
        rhs = "(K1 TSRK K0) ADDK (K2 TSRK K0)",
        rewrite_method=ket_tsr_6_rewrite
    )
    rules.append(KET_TSR_6)

    def ket_tsr_7_rewrite(rule, term, side_info):
        if isinstance(term, KetTensor) and isinstance(term.args[1], KetAdd):
            new_args = tuple(KetTensor(term[0], arg) for arg in term.args[1].args)
            return KetAdd(*new_args)
    KET_TSR_7 = TRSRule(
        lhs = "K0 TSRK (K1 ADDK K2)",
        rhs = "(K0 TSRK K1) ADDK (K0 TSRK K2)",
        rewrite_method=ket_tsr_7_rewrite
    )
    rules.append(KET_TSR_7)


    ###################################################
    # Bra


    BRA_ADJ_1 = TRSRule(
        lhs = parse(r'''ADJB(0K)'''),
        rhs = parse(r'''0B''')
    )
    rules.append(BRA_ADJ_1)

    BRA_ADJ_2 = TRSRule(
        lhs = parse(r'''ADJB(KET(s))'''),
        rhs = parse(r'''BRA(s)''')
    )
    rules.append(BRA_ADJ_2)

    BRA_ADJ_3 = TRSRule(
        lhs = parse(r'''ADJB(ADJK(B0))'''),
        rhs = parse(r'''B0''')
    )
    rules.append(BRA_ADJ_3)

    BRA_ADJ_4 = TRSRule(
        lhs = parse(r'''ADJB(S0 SCRK K0)'''),
        rhs = parse(r'''CONJS(S0) SCRB ADJB(K0)'''),
    )
    rules.append(BRA_ADJ_4)

    def bra_adj_5_rewrite(rule, term, side_info):
        if isinstance(term, BraAdj):
            if isinstance(term.args[0], KetAdd):
                new_args = tuple(BraAdj(arg) for arg in term.args[0].args)
                return BraAdd(*new_args)
    BRA_ADJ_5 = TRSRule(
        lhs = "ADJB(K1 ADDK K2)",
        rhs = "ADJB(K1) ADDB ADJB(K2)",
        rewrite_method=bra_adj_5_rewrite
    )
    rules.append(BRA_ADJ_5)

    BRA_ADJ_6 = TRSRule(
        lhs = parse(r'''ADJB(O0 MLTK K0)'''),
        rhs = parse(r'''ADJB(K0) MLTB ADJO(O0)''')
    )
    rules.append(BRA_ADJ_6)

    BRA_ADJ_7 = TRSRule(
        lhs = parse(r''' ADJB(K1 TSRK K2) '''),
        rhs = parse(r''' ADJB(K1) TSRB ADJB(K2) ''')
    )
    rules.append(BRA_ADJ_7)



    BRA_SCAL_1 = TRSRule(
        lhs = parse(r''' "0" SCRB B0 '''),
        rhs = parse(r''' 0B '''),
        rule_repr = '''C(0) SCRB B0 -> 0B ;'''
    )
    rules.append(BRA_SCAL_1)

    BRA_SCAL_2 = TRSRule(
        lhs = parse(r''' "1" SCRB B0 '''),
        rhs = parse(r''' B0 '''),
        rule_repr = '''C(1) SCRB B0 -> B0 ;'''
    )
    rules.append(BRA_SCAL_2)

    BRA_SCAL_3 = TRSRule(
        lhs = parse(r'''S0 SCRB 0B'''),
        rhs = parse(r''' 0B ''')
    )
    rules.append(BRA_SCAL_3)

        
    BRA_SCAL_4 = TRSRule(
        lhs = parse(r'''S1 SCRB (S2 SCRB B0)'''),
        rhs = parse(r'''(S1 MLTS S2) SCRB B0'''),
    )
    rules.append(BRA_SCAL_4)


    def bra_scal_5_rewrite(rule, term, side_info):
        if isinstance(term, BraScal):
            if isinstance(term.args[1], BraAdd):
                new_args = tuple(BraScal(term.args[0], arg) for arg in term.args[1].args)
                return BraAdd(*new_args)
            
    BRA_SCAL_5 = TRSRule(
        lhs = "S0 SCRB (B1 ADDB B2)",
        rhs = "(S0 SCRB B1) ADDB (S0 SCRB B2)",
        rewrite_method=bra_scal_5_rewrite
    )
    rules.append(BRA_SCAL_5)



    def bra_add_1(rule, term, side_info):
        if isinstance(term, BraAdd):
            for i in range(len(term.args)):
                if term.args[i] == BraZero():
                    return BraAdd(*term.remained_terms(i))
    BRA_ADD_1 = TRSRule(
        lhs = "0B ADDB B0",
        rhs = "B0",
        rewrite_method=bra_add_1
    )
    rules.append(BRA_ADD_1)

    def bra_add_2(rule, term, side_info):
        if isinstance(term, BraAdd):
            for i in range(len(term.args)):
                for j in range(i+1, len(term.args)):
                    if term.args[i] == term.args[j]:
                        new_args = (BraScal(C2, term.args[i]),) + term.remained_terms(i, j)
                        return BraAdd(*new_args)
    BRA_ADD_2 = TRSRule(
        lhs = "B0 ADDB B0",
        rhs = "C(1 + 1) SCRB B0",
        rewrite_method=bra_add_2
    )
    rules.append(BRA_ADD_2)

    def bra_add_3(rule, term, side_info):
        if isinstance(term, BraAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], BraScal):
                    for j in range(len(term.args)):
                        if term.args[i].args[1] == term.args[j]:
                            new_args = (
                                BraScal(ScalarAdd(term.args[i].args[0], C1), term.args[j]),) + term.remained_terms(i, j)
                            return BraAdd(*new_args)
    BRA_ADD_3 = TRSRule(
        lhs = "(S0 SCRB B0) ADDB B0",
        rhs = "(S0 ADDS C(1)) SCRB B0",
        rewrite_method=bra_add_3
    )
    rules.append(BRA_ADD_3)


    def bra_add_4(rule, term, side_info):
        if isinstance(term, BraAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], BraScal):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], BraScal):
                            if term.args[i].args[1] == term.args[j].args[1]:
                                new_args = (BraScal(ScalarAdd(term.args[i].args[0], term.args[j].args[0]), term.args[i].args[1]),) + term.remained_terms(i, j)
                                return BraAdd(*new_args)
    BRA_ADD_4 = TRSRule(
        lhs = "(S1 SCRB B0) ADDB (S2 SCRB B0)",
        rhs = "(S1 ADDS S2) SCRB B0",
        rewrite_method=bra_add_4
    )
    rules.append(BRA_ADD_4)


    BRA_MUL_1 = TRSRule(
        lhs = parse(r'''B0 MLTB 0O'''),
        rhs = parse(r'''0B''')
    )
    rules.append(BRA_MUL_1)

    BRA_MUL_2 = TRSRule(
        lhs = parse(r'''0B MLTB O0'''),
        rhs = parse(r'''0B''')
    )
    rules.append(BRA_MUL_2)

    BRA_MUL_3 = TRSRule(
        lhs = parse(r'''B0 MLTB 1O'''),
        rhs = parse(r'''B0''')
    )
    rules.append(BRA_MUL_3)

    BRA_MUL_4 = TRSRule(
        lhs = parse(r'''B0 MLTB (S0 SCRO O0)'''),
        rhs = parse(r'''S0 SCRB (B0 MLTB O0)''')
    )
    rules.append(BRA_MUL_4)

    BRA_MUL_5 = TRSRule(
        lhs = parse(r'''(S0 SCRB B0) MLTB O0'''),
        rhs = parse(r'''S0 SCRB (B0 MLTB O0)''')
    )
    rules.append(BRA_MUL_5)


    def bra_mul_6_rewrite(rule, term, side_info):
        if isinstance(term, BraApply) and isinstance(term.args[1], OpAdd):
            new_args = tuple(BraApply(term[0], arg) for arg in term.args[1].args)
            return BraAdd(*new_args)


    BRA_MUL_6 = TRSRule(
        lhs = "B0 MLTB (O1 ADDO O2)",
        rhs = "(B0 MLTB O1) ADDB (B0 MLTB O2)",
        rewrite_method=bra_mul_6_rewrite
    )
    rules.append(BRA_MUL_6)


    def bra_mul_7_rewrite(rule, term, side_info):
        if isinstance(term, BraApply) and isinstance(term.args[0], BraAdd):
            new_args = tuple(BraApply(arg, term[1]) for arg in term.args[0].args)
            return BraAdd(*new_args)
    BRA_MUL_7 = TRSRule(
        lhs = "(B1 ADDB B2) MLTB O0",
        rhs = "(B1 MLTB O0) ADDB (B2 MLTB O0)",
        rewrite_method=bra_mul_7_rewrite
    )
    rules.append(BRA_MUL_7)

    BRA_MUL_8 = TRSRule(
        lhs = parse(r'''B1 MLTB (K1 OUTER B2)'''),
        rhs = parse(r'''(B1 DOT K1) SCRB B2''')
    )
    rules.append(BRA_MUL_8)

    BRA_MUL_9 = TRSRule(
        lhs = parse(r'''B0 MLTB (O1 MLTO O2)'''),
        rhs = parse(r'''(B0 MLTB O1) MLTB O2''')
    )
    rules.append(BRA_MUL_9)


    BRA_MUL_10 = TRSRule(
        lhs = parse(r'''(B0 MLTB (O1 TSRO O2)) MLTB (O1_ TSRO O2_)'''),
        rhs = parse(r'''B0 MLTB ((O1 MLTO O1_) TSRO (O2 MLTO O2_))''')
    )
    rules.append(BRA_MUL_10)

    BRA_MUL_11 = TRSRule(
        lhs = parse(r'''BRA(t) MLTB (O1 TSRO O2)'''),
        rhs = parse(r'''(BRA(FST(t)) MLTB O1) TSRB (BRA(SND(t)) MLTB O2)''')
    )
    rules.append(BRA_MUL_11)

    BRA_MUL_12 = TRSRule(
        lhs = parse(r'''(B1 TSRB B2) MLTB (O1 TSRO O2)'''),
        rhs = parse(r'''(B1 MLTB O1) TSRB (B2 MLTB O2)''')
    )
    rules.append(BRA_MUL_12)



    BRA_TSR_1 = TRSRule(
        lhs = parse(r'''0B TSRB B0'''),
        rhs = parse(r'''0B''')
    )
    rules.append(BRA_TSR_1)

    BRA_TSR_2 = TRSRule(
        lhs = parse(r'''B0 TSRB 0B'''),
        rhs = parse(r'''0B''')
    )
    rules.append(BRA_TSR_2)

    BRA_TSR_3 = TRSRule(
        lhs = parse(r'''BRA(s) TSRB BRA(t)'''),
        rhs = parse(r'''BRA(PAIR(s, t))''')
    )
    rules.append(BRA_TSR_3)

    BRA_TSR_4 = TRSRule(
        lhs = parse(r'''(S0 SCRB B1) TSRB B2'''),
        rhs = parse(r'''S0 SCRB (B1 TSRB B2)''')
    )
    rules.append(BRA_TSR_4)

    BRA_TSR_5 = TRSRule(
        lhs = parse(r'''B1 TSRB (S0 SCRB B2)'''),
        rhs = parse(r'''S0 SCRB (B1 TSRB B2)''')
    )
    rules.append(BRA_TSR_5)

    def bra_tsr_6_rewrite(rule, term, side_info):
        if isinstance(term, BraTensor) and isinstance(term.args[0], BraAdd):
            new_args = tuple(BraTensor(arg, term[1]) for arg in term.args[0].args)
            return BraAdd(*new_args)
    BRA_TSR_6 = TRSRule(
        lhs = "(B1 ADDB B2) TSRB B0",
        rhs = "(B1 TSRB B0) ADDB (B2 TSRB B0)",
        rewrite_method=bra_tsr_6_rewrite
    )
    rules.append(BRA_TSR_6)

    def bra_tsr_7_rewrite(rule, term, side_info):
        if isinstance(term, BraTensor) and isinstance(term.args[1], BraAdd):
            new_args = tuple(BraTensor(term[0], arg) for arg in term.args[1].args)
            return BraAdd(*new_args)
    BRA_TSR_7 = TRSRule(
        lhs = "B0 TSRB (B1 ADDB B2)",
        rhs = "(B0 TSRB B1) ADDB (B0 TSRB B2)",
        rewrite_method=bra_tsr_7_rewrite
    )
    rules.append(BRA_TSR_7)


    ###########################################################
    # Operators

    OPT_OUTER_1 = TRSRule(
        lhs = parse(r'''0K OUTER B0 '''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_OUTER_1)

    OPT_OUTER_2 = TRSRule(
        lhs = parse(r'''K0 OUTER 0B'''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_OUTER_2)

    OPT_OUTER_3 = TRSRule(
        lhs = parse(r'''(S0 SCRK K0) OUTER B0'''),
        rhs = parse(r'''S0 SCRO (K0 OUTER B0)''')
    )
    rules.append(OPT_OUTER_3)

    OPT_OUTER_4 = TRSRule(
        lhs = parse(r'''K0 OUTER (S0 SCRB B0)'''),
        rhs = parse(r'''S0 SCRO (K0 OUTER B0)''')
    )
    rules.append(OPT_OUTER_4)

    def opt_outer_5_rewrite(rule, term, side_info):
        if isinstance(term, OpOuter) and isinstance(term.args[0], KetAdd):
            new_args = tuple(OpOuter(arg, term[1]) for arg in term.args[0].args)
            return OpAdd(*new_args)
    OPT_OUTER_5 = TRSRule(
        lhs = "(K1 ADDK K2) OUTER B0",
        rhs = "(K1 OUTER B0) ADDO (K2 OUTER B0)",
        rewrite_method=opt_outer_5_rewrite
    )
    rules.append(OPT_OUTER_5)

    def opt_outer_6_rewrite(rule, term, side_info):
        if isinstance(term, OpOuter) and isinstance(term.args[1], BraAdd):
            new_args = tuple(OpOuter(term[0], arg) for arg in term.args[1].args)
            return OpAdd(*new_args)
    OPT_OUTER_6 = TRSRule(
        lhs = "K0 OUTER (B1 ADDB B2)",
        rhs = "(K0 OUTER B1) ADDO (K0 OUTER B2)",
        rewrite_method=opt_outer_6_rewrite
    )
    rules.append(OPT_OUTER_6)


    OPT_ADJ_1 = TRSRule(
        lhs = parse(r'''ADJO(0O)'''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_ADJ_1)

    OPT_ADJ_2 = TRSRule(
        lhs = parse(r'''ADJO(1O)'''),
        rhs = parse(r'''1O''')
    )
    rules.append(OPT_ADJ_2)

    OPT_ADJ_3 = TRSRule(
        lhs = parse(r'''ADJO(K0 OUTER B0)'''),
        rhs = parse(r'''ADJK(B0) OUTER ADJB(K0)''')
    )
    rules.append(OPT_ADJ_3)

    OPT_ADJ_4 = TRSRule(
        lhs = parse(r'''ADJO(ADJO(O0))'''),
        rhs = parse(r'''O0''')
    )
    rules.append(OPT_ADJ_4)

    OPT_ADJ_5 = TRSRule(
        lhs = parse(r'''ADJO(S0 SCRO O0)'''),
        rhs = parse(r'''CONJS(S0) SCRO ADJO(O0)''')
    )
    rules.append(OPT_ADJ_5)

    def opt_adj_6_rewrite(rule, term, side_info):
        if isinstance(term, OpAdj):
            if isinstance(term.args[0], OpAdd):
                new_args = tuple(OpAdj(arg) for arg in term.args[0].args)
                return OpAdd(*new_args)
    OPT_ADJ_6 = TRSRule(
        lhs = "ADJO(O1 ADDO O2)",
        rhs = "ADJO(O1) ADDO ADJO(O2)",
        rewrite_method=opt_adj_6_rewrite
    )
    rules.append(OPT_ADJ_6)

    OPT_ADJ_7 = TRSRule(
        lhs = parse(r'''ADJO(O1 MLTO O2)'''),
        rhs = parse(r'''ADJO(O2) MLTO ADJO(O1)''')
    )
    rules.append(OPT_ADJ_7)


    OPT_ADJ_8 = TRSRule(
        lhs = parse(r'''ADJO(O1 TSRO O2)'''),
        rhs = parse(r'''ADJO(O1) TSRO ADJO(O2)''')
    )
    rules.append(OPT_ADJ_8)


    OPT_SCAL_1 = TRSRule(
        lhs = parse(r''' "0" SCRO O0'''),
        rhs = parse(r'''0O'''),
        rule_repr = '''C(0) SCRO O0 -> 0O ;'''
    )
    rules.append(OPT_SCAL_1)

    OPT_SCAL_2 = TRSRule(
        lhs = parse(r''' "1" SCRO O0'''),
        rhs = parse(r'''O0'''),
        rule_repr = '''C(1) SCRO O0 -> O0 ;'''
    )
    rules.append(OPT_SCAL_2)

    OPT_SCAL_3 = TRSRule(
        lhs = parse(r'''S0 SCRO 0O'''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_SCAL_3)

    OPT_SCAL_4 = TRSRule(
        lhs = parse(r'''S1 SCRO (S2 SCRO O0)'''),
        rhs = parse(r'''(S1 MLTS S2) SCRO O0''')
    )
    rules.append(OPT_SCAL_4)

    def opt_scal_5_rewrite(rule, term, side_info):
        if isinstance(term, OpScal):
            if isinstance(term.args[1], OpAdd):
                new_args = tuple(OpScal(term.args[0], arg) for arg in term.args[1].args)
                return OpAdd(*new_args)
    OPT_SCAL_5 = TRSRule(
        lhs = "S0 SCRO (O1 ADDO O2)",
        rhs = "(S0 SCRO O1) ADDO (S0 SCRO O2)",
        rewrite_method=opt_scal_5_rewrite
    )
    rules.append(OPT_SCAL_5)


    def opt_add_1_rewrite(rule, term, side_info):
        if isinstance(term, OpAdd):
            for i in range(len(term.args)):
                if term.args[i] == OpZero():
                    return OpAdd(*term.remained_terms(i))
    OPT_ADD_1 = TRSRule(
        lhs = "0O ADDO O0",
        rhs = "O0",
        rewrite_method=opt_add_1_rewrite
    )
    rules.append(OPT_ADD_1)


    def opt_add_2_rewrite(rule, term, side_info):
        if isinstance(term, OpAdd):
            for i in range(len(term.args)):
                for j in range(i+1, len(term.args)):
                    if term.args[i] == term.args[j]:
                        new_args = (OpScal(C2, term.args[i]),) + term.remained_terms(i, j)
                        return OpAdd(*new_args)
    OPT_ADD_2 = TRSRule(
        lhs = "O0 ADDO O0",
        rhs = "C(1 + 1) SCRO O0",
        rewrite_method=opt_add_2_rewrite
    )
    rules.append(OPT_ADD_2)

    def opt_add_3_rewrite(rule, term, side_info):
        if isinstance(term, OpAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], OpScal):
                    for j in range(len(term.args)):
                        if term.args[i].args[1] == term.args[j]:
                            new_args = (
                                OpScal(ScalarAdd(term.args[i].args[0], C1), term.args[j]),) + term.remained_terms(i, j)
                            return OpAdd(*new_args)
    OPT_ADD_3 = TRSRule(
        lhs = "(S0 SCRO O0) ADDO O0",
        rhs = "(S0 ADDS C(1)) SCRO O0",
        rewrite_method=opt_add_3_rewrite
    )
    rules.append(OPT_ADD_3)

    def opt_add_4_rewrite(rule, term, side_info):
        if isinstance(term, OpAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], OpScal):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], OpScal):
                            if term.args[i].args[1] == term.args[j].args[1]:
                                new_args = (OpScal(ScalarAdd(term.args[i].args[0], term.args[j].args[0]), term.args[i].args[1]),) + term.remained_terms(i, j)
                                return OpAdd(*new_args)
    OPT_ADD_4 = TRSRule(
        lhs = "(S1 SCRO O0) ADDO (S2 SCRO O0)",
        rhs = "(S1 ADDS S2) SCRO O0",
        rewrite_method=opt_add_4_rewrite
    )
    rules.append(OPT_ADD_4)


    OPT_MUL_1 = TRSRule(
        lhs = parse(r'''0O MLTO O0'''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_MUL_1)

    OPT_MUL_2 = TRSRule(
        lhs = parse(r'''O0 MLTO 0O'''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_MUL_2)

    OPT_MUL_3 = TRSRule(
        lhs = parse(r'''1O MLTO O0'''),
        rhs = parse(r'''O0''')
    )
    rules.append(OPT_MUL_3)

    OPT_MUL_4 = TRSRule(
        lhs = parse(r'''O0 MLTO 1O'''),
        rhs = parse(r'''O0''')
    )
    rules.append(OPT_MUL_4)

    OPT_MUL_5 = TRSRule(
        lhs = parse(r'''(K0 OUTER B0) MLTO O0'''),
        rhs = parse(r'''K0 OUTER (B0 MLTB O0)''')
    )
    rules.append(OPT_MUL_5)

    OPT_MUL_6 = TRSRule(
        lhs = parse(r'''O0 MLTO (K0 OUTER B0)'''),
        rhs = parse(r'''(O0 MLTK K0) OUTER B0''')
    )
    rules.append(OPT_MUL_6)

    OPT_MUL_7 = TRSRule(
        lhs = parse(r'''(S0 SCRO O1) MLTO O2'''),
        rhs = parse(r'''S0 SCRO (O1 MLTO O2)''')
    )
    rules.append(OPT_MUL_7)

    OPT_MUL_8 = TRSRule(
        lhs = parse(r'''O1 MLTO (S0 SCRO O2)'''),
        rhs = parse(r'''S0 SCRO (O1 MLTO O2)''')
    )
    rules.append(OPT_MUL_8)

    def opt_mul_9_rewrite(rule, term, side_info):
        if isinstance(term, OpApply) and isinstance(term.args[0], OpAdd):
            new_args = tuple(OpApply(arg, term[1]) for arg in term.args[0].args)
            return OpAdd(*new_args)
    OPT_MUL_9 = TRSRule(
        lhs = "(O1 ADDO O2) MLTO O0",
        rhs = "(O1 MLTO O0) ADDO (O2 MLTO O0)",
        rewrite_method=opt_mul_9_rewrite
    )
    rules.append(OPT_MUL_9)

    def opt_mul_10_rewrite(rule, term, side_info):
        if isinstance(term, OpApply) and isinstance(term.args[1], OpAdd):
            new_args = tuple(OpApply(term[0], arg) for arg in term.args[1].args)
            return OpAdd(*new_args)
    OPT_MUL_10 = TRSRule(
        lhs = "O0 MLTO (O1 ADDO O2)",
        rhs = "(O0 MLTO O1) ADDO (O0 MLTO O2)",
        rewrite_method=opt_mul_10_rewrite
    )
    rules.append(OPT_MUL_10)

    OPT_MUL_11 = TRSRule(
        lhs = parse(r'''(O1 MLTO O2) MLTO O3'''),
        rhs = parse(r'''O1 MLTO (O2 MLTO O3)''')
    )
    rules.append(OPT_MUL_11)

    OPT_MUL_12 = TRSRule(
        lhs = parse(r'''(O1 TSRO O2) MLTO (O1_ TSRO O2_)'''),
        rhs = parse(r'''(O1 MLTO O1_) TSRO (O2 MLTO O2_)''')
    )
    rules.append(OPT_MUL_12)

    OPT_MUL_13 = TRSRule(
        lhs = parse(r'''(O1 TSRO O2) MLTO ((O1_ TSRO O2_) MLTO O3)'''),
        rhs = parse(r'''((O1 MLTO O1_) TSRO (O2 MLTO O2_)) MLTO O3''')
    )
    rules.append(OPT_MUL_13)


    OPT_TSR_1 = TRSRule(
        lhs = parse(r'''0O TSRO O0'''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_TSR_1)

    OPT_TSR_2 = TRSRule(
        lhs = parse(r'''O0 TSRO 0O'''),
        rhs = parse(r'''0O''')
    )
    rules.append(OPT_TSR_2)

    OPT_TSR_3 = TRSRule(
        lhs = parse(r'''(K1 OUTER B1) TSRO (K2 OUTER B2)'''),
        rhs = parse(r'''(K1 TSRK K2) OUTER (B1 TSRB B2)''')
    )
    rules.append(OPT_TSR_3)

    OPT_TSR_4 = TRSRule(
        lhs = parse(r'''(S0 SCRO O1) TSRO O2'''),
        rhs = parse(r'''S0 SCRO (O1 TSRO O2)''')
    )
    rules.append(OPT_TSR_4)

    OPT_TSR_5 = TRSRule(
        lhs = parse(r'''O1 TSRO (S0 SCRO O2)'''),
        rhs = parse(r'''S0 SCRO (O1 TSRO O2)''')
    )
    rules.append(OPT_TSR_5)

    def opt_tsr_6_rewrite(rule, term, side_info):
        if isinstance(term, OpTensor) and isinstance(term.args[0], OpAdd):
            new_args = tuple(OpTensor(arg, term[1]) for arg in term.args[0].args)
            return OpAdd(*new_args)
    OPT_TSR_6 = TRSRule(
        lhs = "(O1 ADDO O2) TSRO O0",
        rhs = "(O1 TSRO O0) ADDO (O2 TSRO O0)",
        rewrite_method=opt_tsr_6_rewrite
    )
    rules.append(OPT_TSR_6)

    def opt_tsr_7_rewrite(rule, term, side_info):
        if isinstance(term, OpTensor) and isinstance(term.args[1], OpAdd):
            new_args = tuple(OpTensor(term[0], arg) for arg in term.args[1].args)
            return OpAdd(*new_args)
    OPT_TSR_7 = TRSRule(
        lhs = "O0 TSRO (O1 ADDO O2)",
        rhs = "(O0 TSRO O1) ADDO (O0 TSRO O2)",
        rewrite_method=opt_tsr_7_rewrite
    )
    rules.append(OPT_TSR_7)



    # build the trs
    return TRS(rules)


##################################
# output the CiME2 checking code

def dirac_cime2_file(trs: TRS, path: str):
    code = f'''
(* 

    Language and Term Rewriting System for "Typed Dirac Notation"

    This language can be used in two levels: deal with the internal untyped language directly,
    or use the typed syntax with type polymorphism.

    Yingte Xu, 2024

    Automatically generated by diracdec/theory/dirac/trs.py
    Time: {datetime.datetime.now()}

*)

let F = signature
"

  (* complex number *)
  + : AC ;
  * : AC ;
  0 : constant ;
  1 : constant ;
  ^* : postfix unary ;

  (* -------- types -------- *)
  T : constant ;
  PROD : infix binary ;

  Base : binary ;
  S : unary ;
  K : binary ;
  B : binary ;
  O : 3 ;
  

  (* -------- syntax symbols -------- *)
  (* The external language. Will be be transformed in to the internal langauge during type checking. *)

  (* Basis *)
  PAIR_S : binary ;
  FST_S : unary ;
  SND_S : unary ;

  (* Scalar *)
  C_S : unary ;
  DELTA_S : binary ;
  ADDS_S : infix binary ;
  MLTS_S : infix binary ;
  CONJS_S : unary ;
  DOT_S : infix binary ;

  (* Ket *)
  0K_S : unary ;
  KET_S : unary ;
  ADJK_S : unary ;
  SCRK_S : infix binary ;
  ADDK_S : infix binary ;
  MLTK_S : infix binary ;
  TSRK_S : infix binary ;

  (* Bra *)
  0B_S : unary ;
  BRA_S : unary ;
  ADJB_S : unary ;
  SCRB_S : infix binary ;
  ADDB_S : infix binary ;
  MLTB_S : infix binary ;
  TSRB_S : infix binary ;

  (* Operator *)
  0O_S : binary ;
  1O_S : unary ;
  OUTER_S : infix binary ;
  ADJO_S : unary ;
  SCRO_S : infix binary ;
  ADDO_S : infix binary ;
  MLTO_S : infix binary ;
  TSRO_S : infix binary ;

  (* universal application *)
  @ : infix binary ;

  (* otimes and cdot *)
  OTIMES : infix binary ;
  CDOT : infix binary ;


  (* -------- internal langauge -------- *)

  (* Basis *)
  PAIR : binary ;
  FST : unary ;
  SND : unary ;

  (* Scalar *)
  C : unary ;
  DELTA : commutative ;
  ADDS : AC ;
  MLTS : AC ;
  CONJS : unary ;
  DOT : infix binary ;

  (* Ket *)
  0K : constant ;
  KET : unary ;
  ADJK : unary ;
  SCRK : infix binary ;
  ADDK : AC ;
  MLTK : infix binary ;
  TSRK : infix binary ;

  (* Bra *)
  0B : constant ;
  BRA : unary ;
  ADJB : unary ;
  SCRB : infix binary ;
  ADDB : AC ;
  MLTB : infix binary ;
  TSRB : infix binary ;

  (* Operator *)
  0O : constant ;
  1O : constant ;
  OUTER : infix binary ;
  ADJO : unary ;
  SCRO : infix binary ;
  ADDO : AC ;
  MLTO : infix binary ;
  TSRO : infix binary ;

";

let X = vars "a b c x S0 S1 S2 S3 s s1 s2 t t1 t2 B0 B1 B2 K0 K1 K2 O0 O1 O2 O1' O2' T1 T2 T3 T4 O1_ O2_ O3";

let R = TRS F X "

  (* ######################## TYPE CHECKING ############################ *)
  C_S(a) -> S(C(a)) ;
  DELTA_S(Base(s, T1), Base(t, T1)) -> S(DELTA(s, t)) ;
  S(a) ADDS_S S(b) -> S(a ADDS b) ;
  S(a) MLTS_S S(b) -> S(a MLTS b) ;
  CONJS_S(S(a)) -> S(CONJS(a)) ;
  B(B0, T1) DOT_S K(K0, T1) -> S(B0 DOT K0) ;

  (* Ket *)
  0K_S(T1) -> K(0K, T1) ;
  KET_S(Base(s, T1)) -> K(KET(s), T1) ;
  ADJK_S(B(B0, T1)) -> K(ADJK(B0), T1) ;
  S(S0) SCRK_S K(K0, T1) -> K(S0 SCRK K0, T1) ;
  K(K1, T1) ADDK_S K(K2, T1) -> K(K1 ADDK K2, T1) ;
  O(O0, T1, T2) MLTK_S K(K0, T2) -> K(O0 MLTK K0, T1) ;
  K(K1, T1) TSRK_S K(K2, T2) -> K(K1 TSRK K2, T1 PROD T2) ;

  (* Bra *)
  0B_S(T1) -> B(0B, T1) ;
  BRA_S(Base(s, T1)) -> B(BRA(s), T1) ;
  ADJB_S(K(K0, T1)) -> B(ADJB(K0), T1) ;
  S(S0) SCRB_S B(B0, T1) -> B(S0 SCRB B0, T1) ;
  B(B1, T1) ADDB_S B(B2, T1) -> B(B1 ADDB B2, T1) ;
  B(B0, T1) MLTB_S O(O0, T1, T2) -> B(B0 MLTB O0, T2) ;
  B(B1, T1) TSRB_S B(B2, T2) -> B(B1 TSRB B2, T1 PROD T2) ;

  (* Operator *)
  0O_S(T1, T2) -> O(0O, T1, T2) ;
  1O_S(T1) -> O(1O, T1, T1) ;
  K(K0, T1) OUTER_S B(B0, T2) -> O(K0 OUTER B0, T1, T2) ;
  ADJO_S(O(O0, T1, T2)) -> O(ADJO(O0), T2, T1) ;
  S(S0) SCRO_S O(O0, T1, T2) -> O(S0 SCRO O0, T1, T2) ;
  O(O1, T1, T2) ADDO_S O(O2, T1, T2) -> O(O1 ADDO O2, T1, T2) ;
  O(O1, T1, T2) MLTO_S O(O2, T2, T3) -> O(O1 MLTO O2, T1, T3) ;
  O(O1, T1, T2) TSRO_S O(O2, T3, T4) -> O(O1 TSRO O2, T1 PROD T3, T2 PROD T4) ;

  (* -------- overload the universal application --------- *)
  S(S1) @ S(S2) -> S(S1 MLTS S2) ;
  S(S0) @ K(K0, T1) -> K(S0 SCRK K0, T1) ;
  S(S0) @ B(B0, T1) -> B(S0 SCRB B0, T1) ;

  S(S0) @ O(O0, T1, T2) -> O(S0 SCRO O0, T1, T2) ;
  K(K0, T1) @ S(S0) -> K(S0 SCRK K0, T1) ;
  K(K1, T1) @ K(K2, T2) -> K(K1 TSRK K2, T1 PROD T2) ;
  K(K0, T1) @ B(B0, T2) -> O(K0 OUTER B0, T1, T2) ;

  B(B0, T1) @ S(S0) -> B(S0 SCRB B0, T1) ;
  B(B0, T1) @ K(K0, T1) -> S(B0 DOT K0) ;
  B(B1, T1) @ B(B2, T2) -> B(B1 TSRB B2, T1 PROD T2) ;
  B(B0, T1) @ O(O0, T1, T2) -> B(B0 MLTB O0, T2) ;

  O(O0, T1, T2) @ S(S0) -> O(S0 SCRO O0, T1, T2) ;
  O(O0, T1, T2) @ K(K0, T2) -> K(O0 MLTK K0, T1) ;
  O(O1, T1, T2) @ O(O2, T2, T3) -> O(O1 MLTO O2, T1, T3) ;

  (* -------- overload of otimes and cdot -------- *)
  K(K1, T1) OTIMES K(K2, T2) -> K(K1 TSRK K2, T1 PROD T2) ;
  B(B1, T1) OTIMES B(B2, T2) -> B(B1 TSRB B2, T1 PROD T2) ;
  K(K0, T1) OTIMES B(B0, T2) -> O(K0 OUTER B0, T1, T2) ;
  O(O1, T1, T2) OTIMES O(O2, T3, T4) -> O(O1 TSRO O2, T1 PROD T3, T2 PROD T4) ;

  B(B0, T1) CDOT O(O0, T1, T2) -> B(B0 MLTB O0, T2) ;
  O(O0, T1, T2) CDOT K(K0, T2) -> K(O0 MLTK K0, T1) ;
  B(B0, T1) CDOT K(K0, T1) -> S(B0 DOT K0) ;
  O(O1, T1, T2) CDOT O(O2, T2, T3) -> O(O1 MLTO O2, T1, T3) ;




  (* ############# REDUCTION RULES FOR INTERNAL LANGUAGE ############### *)

  (********************************************)
  (*           complex number (avatar)        *)
  (********************************************)

  0 + a -> a ;
  0 * a -> 0 ;
  1 * a -> a ;
  a * (b + c) -> (a * b) + (a * c) ;
  0 ^* -> 0 ;
  1 ^* -> 1 ;
  (a + b) ^* -> (a ^*) + (b ^*) ;
  (a * b) ^* -> (a ^*) * (b ^*) ;
  (a ^*) ^* -> a ;

(* >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> *)
(* PUT PYTHON CIME OUTPUT IN BETWEEN *)

{trs.CiME2_rules()}

(* PUT PYTHON CIME OUTPUT IN BETWEEN *)
(* <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< *)
  
  (* ################# extension rules for AC symbols ################## *)

  (* To prove the confluence of a system with AC symbols, we need to check the critical pairs of an extended system. *)

  (0 + a) + x -> a + x ;
  (0 * a) * x -> 0 * x ;
  (1 * a) * x -> a * x ;
  (a * (b + c)) * x -> ((a * b) + (a * c)) * x ;

  (C(0) ADDS a) ADDS x -> a ADDS x ;
  (C(a) ADDS C(b)) ADDS x -> C(a + b) ADDS x ;
  (S0 ADDS S0) ADDS x -> (C(1 + 1) MLTS S0) ADDS x ;
  ((C(a) MLTS S0) ADDS S0) ADDS x -> (C(a + 1) MLTS S0) ADDS x ;
  ((C(a) MLTS S0) ADDS (C(b) MLTS S0)) ADDS x -> (C(a + b) MLTS S0) ADDS x ;

  (C(0) MLTS a) MLTS x -> C(0) MLTS x ;
  (C(1) MLTS a) MLTS x -> a MLTS x ;
  (C(a) MLTS C(b)) MLTS x -> C(a * b) MLTS x ;
  (S1 MLTS (S2 ADDS S3)) MLTS x -> ((S1 MLTS S2) ADDS (S1 MLTS S3)) MLTS x ;

  (K0 ADDK 0K) ADDK x -> K0 ADDK x ;
  (K0 ADDK K0) ADDK x -> (C(1 + 1) SCRK K0) ADDK x ;
  ((S0 SCRK K0) ADDK K0) ADDK x -> ((S0 ADDS C(1)) SCRK K0) ADDK x ;
  ((S1 SCRK K0) ADDK (S2 SCRK K0)) ADDK x -> ((S1 ADDS S2) SCRK K0) ADDK x ;

  (B0 ADDB 0B) ADDB x -> B0 ADDB x ;
  (B0 ADDB B0) ADDB x -> (C(1 + 1) SCRB B0) ADDB x ;
  ((S0 SCRB B0) ADDB B0) ADDB x -> ((S0 ADDS C(1)) SCRB B0) ADDB x ;
  ((S1 SCRB B0) ADDB (S2 SCRB B0)) ADDB x -> ((S1 ADDS S2) SCRB B0) ADDB x ;

  (O0 ADDO 0O) ADDO x -> O0 ADDO x ;
  (O0 ADDO O0) ADDO x -> (C(1 + 1) SCRO O0) ADDO x ;
  ((S0 SCRO O0) ADDO O0) ADDO x -> ((S0 ADDS C(1)) SCRO O0) ADDO x ;
  ((S1 SCRO O0) ADDO (S2 SCRO O0)) ADDO x -> ((S1 ADDS S2) SCRO O0) ADDO x ;
  
";

(* optional : 

  DELTA(s, s) -> C(1) ;

*)
'''
    with open(path, "w") as p:
        p.write(code)