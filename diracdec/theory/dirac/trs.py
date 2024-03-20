
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

def construct_trs(
        CScalar: Type[ComplexScalar], 
        ABase: Type[AtomicBase], 
        parser: yacc.LRParser) -> TRS:
    
    def parse(s: str) -> Term:
        return parser.parse(s)


    # prepare the rules
    rules = []


    C0 = CScalar.zero()
    C1 = CScalar.one()
    C2 = CScalar.add(CScalar.one(), CScalar.one())

    
    #################################################
    # reducing basis and complex scalars

    def atomic_base_rewrite(rule, trs, term):
        if isinstance(term, ABase):
            return term.reduce()
    ATOMIC_BASE = Rule(
        "ATOMIC-BASE",
        lhs = "a",
        rhs = "a",
        rewrite_method=atomic_base_rewrite,
        rule_repr="(* base -> simp(base) *)"
    )
    rules.append(ATOMIC_BASE)

    def complex_scalar_rewrite(rule, trs, term):
        if isinstance(term, CScalar):
            return term.reduce()
    COMPLEX_SCALAR = Rule(
        "COMPLEX-SCALAR",
        lhs = "a",
        rhs = "a",
        rewrite_method=complex_scalar_rewrite,
        rule_repr="(* complex -> simp(complex) *)"
    )
    rules.append(COMPLEX_SCALAR)


    #################################################
    # Base

    BASIS_1 = CanonicalRule(
        "BASIS-1",
        lhs = parse("FST(PAIR(s, t))"),
        rhs = parse("s")
    )
    rules.append(BASIS_1)

    BASIS_2 = CanonicalRule(
        "BASIS-2",
        lhs = parse("SND(PAIR(s, t))"),
        rhs = parse("t")
    )
    rules.append(BASIS_2)

    BASIS_3 = CanonicalRule(
        "BASIS-3",
        lhs = parse("PAIR(FST(s), SND(s))"),
        rhs = parse("s")
    )
    rules.append(BASIS_3)

    #################################################
    # Delta

    DELTA_1 = CanonicalRule(
        "DELTA-1",
        lhs = parse("DELTA(s, PAIR(t1, t2))"),
        rhs = parse("DELTA(FST(s), t1) MLTS DELTA(SND(s), t2)")
    )
    rules.append(DELTA_1)


    DELTA_2 = CanonicalRule(
        "DELTA-2",
        lhs = parse("DELTA(FST(s), FST(t)) MLTS DELTA(SND(s), SND(t))"),
        rhs = parse("DELTA(s, t)")
    )
    rules.append(DELTA_2)


    #################################################
    # Scalar


    SCR_COP_1 = CanonicalRule(
        "SCR-COP-1",
        lhs=parse(''' "0" ADDS a '''), 
        rhs=parse(''' a ''')
    )
    rules.append(SCR_COP_1)


    def scr_cop_2_rewrite(rule, trs, term):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ComplexScalar):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], ComplexScalar):

                            new_args = (CScalar.add(term.args[i], term.args[j]),) + term.remained_terms(i, j)

                            return ScalarAdd(*new_args)

    SCR_COP_2 = Rule(
        "SCR-COP-2",
        lhs="C(a) ADDS C(b)", 
        rhs="C(a + b)",
        rewrite_method=scr_cop_2_rewrite
    )
    rules.append(SCR_COP_2)

                    
    SCR_COP_3 = CanonicalRule(
        "SCR-COP-3",
        lhs = parse(''' S0 ADDS S0 '''),
        rhs = parse(''' "2" MLTS S0 ''')
    )
    rules.append(SCR_COP_3)

    def scr_cop_4_rewrite(rule, trs, term):
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
                                
    SCR_COP_4 = Rule(
        "SCR-COP-4",
        lhs = "(C(a) MLTS S0) ADDS S0",
        rhs = "C(a + 1) MLTS S0",
        rewrite_method=scr_cop_4_rewrite
    )
    rules.append(SCR_COP_4)

    def scr_cop_5_rewrite(rule, trs, term):
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

    SCR_COP_5 = Rule(
        "SCR-COP-5",
        lhs = "(C(a) MLTS S0) ADDS (C(b) MLTS S0)",
        rhs = "C(a + b) MLTS S0",
        rewrite_method=scr_cop_5_rewrite
    )
    rules.append(SCR_COP_5)


    SCR_COP_6 = CanonicalRule(
        "SCR-COP-6",
        lhs=parse(''' "0" MLTS a '''), 
        rhs=parse(''' "0" ''')
    )
    rules.append(SCR_COP_6)

    SCR_COP_7 = CanonicalRule(
        "SCR-COP-7",
        lhs=parse(''' "1" MLTS a '''), 
        rhs=parse(''' a ''')
    )
    rules.append(SCR_COP_7)


    def scr_cop_8_rewrite(rule, trs, term):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ComplexScalar):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], ComplexScalar):

                            new_args = (CScalar.mlt(term.args[i], term.args[j]),) + term.remained_terms(i, j)

                            return ScalarMlt(*new_args)

    SCR_COP_8 = Rule(
        "SCR-COP-8",
        lhs="C(a) MLTS C(b)",
        rhs="C(a * b)",
        rewrite_method=scr_cop_8_rewrite
    )
    rules.append(SCR_COP_8)

    SCR_COP_9 = CanonicalRule(
        "SCR-COP-9",
        lhs= parse("a MLTS (b ADDS c)"),
        rhs= parse("(a MLTS b) ADDS (a MLTS c)")
    )
    rules.append(SCR_COP_9)


    def scr_cop_10_rewrite(rule, trs, term):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ComplexScalar):
                return CScalar.conj(term.args[0])
    SCR_COP_10 = Rule(
        "SCR-COP-10",
        lhs="CONJS(C(a))",
        rhs="C(a ^*)",
        rewrite_method=scr_cop_10_rewrite
    )
    rules.append(SCR_COP_10)
        
            
    SCR_COP_11 = CanonicalRule(
        "SCR-COP-11",
        lhs= parse("CONJS(DELTA(a, b))"),
        rhs= parse("DELTA(a, b)")
    )
    rules.append(SCR_COP_11)


    SCR_COP_12 = CanonicalRule(
        "SCR-COP-12",
        lhs= parse("CONJS(a ADDS b)"),
        rhs= parse("CONJS(a) ADDS CONJS(b)")
    )
    rules.append(SCR_COP_12)


    SCR_COP_13 = CanonicalRule(
        "SCR-COP-13",
        lhs= parse("CONJS(a MLTS b)"),
        rhs= parse("CONJS(a) MLTS CONJS(b)")
    )
    rules.append(SCR_COP_13)


    SCR_COP_14 = CanonicalRule(
        "SCR-COP-14",
        lhs=parse(r''' CONJS(CONJS(a)) '''), 
        rhs=parse(r''' a ''')
    )
    rules.append(SCR_COP_14)

    SCR_COP_15 = CanonicalRule(
        "SCR-COP-15",
        lhs = parse(r''' CONJS(B0 DOT K0) '''),
        rhs = parse(r''' ADJ(K0) DOT ADJ(B0) ''')
    )
    rules.append(SCR_COP_15)


    SCR_DOT_1 = CanonicalRule(
        "SCR-DOT-1",
        lhs = parse(r''' 0X DOT K0 '''),
        rhs = parse(r''' "0" '''),
        rule_repr = '''0X DOT K0 -> C(0) ;'''
    )
    rules.append(SCR_DOT_1)

    SCR_DOT_2 = CanonicalRule(
        "SCR-DOT-2",
        lhs = parse(r''' B0 DOT 0X '''),
        rhs = parse(r''' "0" '''),
        rule_repr = '''B0 DOT 0X -> C(0) ;'''
    )
    rules.append(SCR_DOT_2)

    SCR_DOT_3 = CanonicalRule(
        "SCR-DOT-3",
        lhs = parse(r'''(S0 SCR B0) DOT K0'''),
        rhs = parse(r'''S0 MLTS (B0 DOT K0)''')
    )
    rules.append(SCR_DOT_3)


    SCR_DOT_4 = CanonicalRule(
        "SCR-DOT-4",
        lhs = parse(r'''B0 DOT (S0 SCR K0)'''),
        rhs = parse(r'''S0 MLTS (B0 DOT K0)''')
    )
    rules.append(SCR_DOT_4)


    SCR_DOT_5 = CanonicalRule(
        "SCR-DOT-5",
        lhs = parse("(B1 ADD B2) DOT K0"),
        rhs = parse("(B1 DOT K0) ADDS (B2 DOT K0)")
    )
    rules.append(SCR_DOT_5)


    SCR_DOT_6 = CanonicalRule(
        "SCR-DOT-6",
        lhs = parse("B0 DOT (K1 ADD K2)"),
        rhs = parse("(B0 DOT K1) ADDS (B0 DOT K2)")
    )
    rules.append(SCR_DOT_6)


    SCR_DOT_7 = CanonicalRule(
        "SCR-DOT-7",
        lhs = parse(r''' BRA(s) DOT KET(t) '''),
        rhs = parse(r''' DELTA(s, t) ''')
    )
    rules.append(SCR_DOT_7)


    SCR_DOT_8 = CanonicalRule(
        "SCR-DOT-8",
        lhs = parse(r'''(B1 TSRB B2) DOT KET(t)'''),
        rhs = parse(r'''(B1 DOT KET(FST(t))) MLTS (B2 DOT KET(SND(t)))''')
    )
    rules.append(SCR_DOT_8)

            
    SCR_DOT_9 = CanonicalRule(
        "SCR-DOT-9",
        lhs = parse(r'''BRA(s) DOT (K1 TSRK K2)'''),
        rhs = parse(r'''(BRA(FST(s)) DOT K1) MLTS (BRA(SND(s)) DOT K2)''')
    )
    rules.append(SCR_DOT_9)

            
    SCR_DOT_10 = CanonicalRule(
        "SCR-DOT-10",
        lhs = parse(r'''(B1 TSRB B2) DOT (K1 TSRK K2)'''),
        rhs = parse(r'''(B1 DOT K1) MLTS (B2 DOT K2)'''),
    )
    rules.append(SCR_DOT_10)

    SCR_SORT_1 = CanonicalRule(
        "SCR-SORT-1",
        lhs = parse(r''' (B0 MLTB O0) DOT K0 '''),
        rhs = parse(r''' B0 DOT (O0 MLTK K0) ''')
    )
    rules.append(SCR_SORT_1)

    SCR_SORT_2 = CanonicalRule(
        "SCR-SORT-2",
        lhs = parse(r''' BRA(s) DOT ((O1 TSRO O2) MLTK K0) '''),
        rhs = parse(r''' ((BRA(FST(s)) MLTB O1) TSRB (BRA(SND(s)) MLTB O2)) DOT K0 ''')
    )
    rules.append(SCR_SORT_2)

    SCR_SORT_3 = CanonicalRule(
        "SCR-SORT-3",
        lhs = parse(r''' (B1 TSRB B2) DOT ((O1 TSRO O2) MLTK K0) '''),
        rhs = parse(r''' ((B1 MLTB O1) TSRB (B2 MLTB O2)) DOT K0''')
    )
    rules.append(SCR_SORT_3)


    #######################################
    # unified symbols

    ADJ_UNI_1 = CanonicalRule(
        "ADJ-UNI-1",
        lhs = parse(r'''ADJ(0X)'''),
        rhs = parse(r'''0X''')
    )
    rules.append(ADJ_UNI_1)

    ADJ_UNI_2 = CanonicalRule(
        "ADJ-UNI-2",
        lhs = parse(r'''ADJ(ADJ(X0))'''),
        rhs = parse(r'''X0''')
    )
    rules.append(ADJ_UNI_2)

    ADJ_UNI_3 = CanonicalRule(
        "ADJ-UNI-3",
        lhs = parse(r'''ADJ(S0 SCR X0)'''),
        rhs = parse(r'''CONJS(S0) SCR ADJ(X0)'''),
    )
    rules.append(ADJ_UNI_3)

    
    ADJ_UNI_4 = CanonicalRule(
        "ADJ-UNI-4",
        lhs = parse("ADJ(X1 ADD X2)"),
        rhs = parse("ADJ(X1) ADD ADJ(X2)")
    )
    rules.append(ADJ_UNI_4)


    ADJ_KET_1 = CanonicalRule(
        "ADJ-KET-1",
        lhs = parse(r'''ADJ(BRA(s))'''),
        rhs = parse(r'''KET(s)''')
    )
    rules.append(ADJ_KET_1)

    ADJ_KET_2 = CanonicalRule(
        "ADJ-KET-2",
        lhs = parse(r'''ADJ(B0 MLTB O0)'''),
        rhs = parse(r'''ADJ(O0) MLTK ADJ(B0)''')
    )
    rules.append(ADJ_KET_2)

    ADJ_KET_3 = CanonicalRule(
        "ADJ-KET-3",
        lhs = parse(r''' ADJ(B1 TSRB B2) '''),
        rhs = parse(r''' ADJ(B1) TSRK ADJ(B2) ''')
    )
    rules.append(ADJ_KET_3)

    ADJ_BRA_1 = CanonicalRule(
        "ADJ-BRA-1",
        lhs = parse(r'''ADJ(KET(s))'''),
        rhs = parse(r'''BRA(s)''')
    )
    rules.append(ADJ_BRA_1)

    ADJ_BRA_2 = CanonicalRule(
        "ADJ-BRA-2",
        lhs = parse(r'''ADJ(O0 MLTK K0)'''),
        rhs = parse(r'''ADJ(K0) MLTB ADJ(O0)''')
    )
    rules.append(ADJ_BRA_2)

    ADJ_BRA_3 = CanonicalRule(
        "ADJ-BRA-3",
        lhs = parse(r''' ADJ(K1 TSRK K2) '''),
        rhs = parse(r''' ADJ(K1) TSRB ADJ(K2) ''')
    )
    rules.append(ADJ_BRA_3)


    ADJ_OPT_1 = CanonicalRule(
        "ADJ-OPT-1",
        lhs = parse(r'''ADJ(1O)'''),
        rhs = parse(r'''1O''')
    )
    rules.append(ADJ_OPT_1)

    ADJ_OPT_2 = CanonicalRule(
        "ADJ-OPT-2",
        lhs = parse(r'''ADJ(K0 OUTER B0)'''),
        rhs = parse(r'''ADJ(B0) OUTER ADJ(K0)''')
    )
    rules.append(ADJ_OPT_2)


    ADJ_OPT_3 = CanonicalRule(
        "ADJ-OPT-3",
        lhs = parse(r'''ADJ(O1 MLTO O2)'''),
        rhs = parse(r'''ADJ(O2) MLTO ADJ(O1)''')
    )
    rules.append(ADJ_OPT_3)


    ADJ_OPT_4 = CanonicalRule(
        "ADJ-OPT-4",
        lhs = parse(r'''ADJ(O1 TSRO O2)'''),
        rhs = parse(r'''ADJ(O1) TSRO ADJ(O2)''')
    )
    rules.append(ADJ_OPT_4)


    SCR_1 = CanonicalRule(
        "SCR-1",
        lhs = parse(r''' "0" SCR X0 '''),
        rhs = parse(r''' 0X '''),
        rule_repr = '''C(0) SCR X0 -> 0X ;'''
    )
    rules.append(SCR_1)


    SCR_2 = CanonicalRule(
        "SCR-2",
        lhs = parse(r''' "1" SCR X0 '''),
        rhs = parse(r''' X0 '''),
        rule_repr = '''C(1) SCR X0 -> X0 ;'''
    )
    rules.append(SCR_2)

    SCR_3 = CanonicalRule(
        "SCR-3",
        lhs = parse(r'''S0 SCR 0X'''),
        rhs = parse(r''' 0X ''')
    )
    rules.append(SCR_3)

        
    SCR_4 = CanonicalRule(
        "SCR-4",
        lhs = parse(r'''S1 SCR (S2 SCR X0)'''),
        rhs = parse(r'''(S1 MLTS S2) SCR X0'''),
    )
    rules.append(SCR_4)

    SCR_5 = CanonicalRule(
        "SCR-5",
        lhs = parse("S0 SCR (X1 ADD X2)"),
        rhs = parse("(S0 SCR X1) ADD (S0 SCR X2)")
    )
    rules.append(SCR_5)


    ADD_1 = CanonicalRule(
        "ADD-1",
        lhs = parse("0X ADD X0"),
        rhs = parse("X0")
    )
    rules.append(ADD_1)

    ADD_2 = CanonicalRule(
        "ADD-2",
        lhs = parse("X0 ADD X0"),
        rhs = parse(''' "2" SCR X0 ''')
    )
    rules.append(ADD_2)

    ADD_3 = CanonicalRule(
        "ADD-3",
        lhs = parse(''' (S0 SCR X0) ADD X0 '''),
        rhs = parse(''' (S0 ADDS "1") SCR X0 ''')
    )
    rules.append(ADD_3)

    ADD_4 = CanonicalRule(
        "ADD-4",
        lhs = parse("(S1 SCR X0) ADD (S2 SCR X0)"),
        rhs = parse("(S1 ADDS S2) SCR X0")
    )
    rules.append(ADD_4)


    #######################################
    # Ket


    KET_MLT_1 = CanonicalRule(
        "KET-MLT-1",
        lhs = parse(r'''0X MLTK K0'''),
        rhs = parse(r'''0X''')
    )
    rules.append(KET_MLT_1)

    KET_MLT_2 = CanonicalRule(
        "KET-MLT-2",
        lhs = parse(r'''O0 MLTK 0X'''),
        rhs = parse(r'''0X''')
    )
    rules.append(KET_MLT_2)

    KET_MLT_3 = CanonicalRule(
        "KET-MLT-3",
        lhs = parse(r'''1O MLTK K0'''),
        rhs = parse(r'''K0''')
    )
    rules.append(KET_MLT_3)

    KET_MLT_4 = CanonicalRule(
        "KET-MLT-4",
        lhs = parse(r'''(S0 SCR O0) MLTK K0'''),
        rhs = parse(r'''S0 SCR (O0 MLTK K0)''')
    )
    rules.append(KET_MLT_4)

    KET_MLT_5 = CanonicalRule(
        "KET-MLT-5",
        lhs = parse(r'''O0 MLTK (S0 SCR K0)'''),
        rhs = parse(r'''S0 SCR (O0 MLTK K0)''')
    )
    rules.append(KET_MLT_5)


    KET_MLT_6 = CanonicalRule(
        "KET-MLT-6",
        lhs = parse("(O1 ADD O2) MLTK K0"),
        rhs = parse("(O1 MLTK K0) ADD (O2 MLTK K0)")
    )
    rules.append(KET_MLT_6)


    KET_MLT_7 = CanonicalRule(
        "KET-MLT-7",
        lhs = parse("O0 MLTK (K1 ADD K2)"),
        rhs = parse("(O0 MLTK K1) ADD (O0 MLTK K2)"),
    )
    rules.append(KET_MLT_7)

    KET_MLT_8 = CanonicalRule(
        "KET-MLT-8",
        lhs = parse(r'''(K1 OUTER B0) MLTK K2'''),
        rhs = parse(r'''(B0 DOT K2) SCR K1''')
    )
    rules.append(KET_MLT_8)

    KET_MLT_9 = CanonicalRule(
        "KET-MLT-9",
        lhs = parse(r'''(O1 MLTO O2) MLTK K0'''),
        rhs = parse(r'''O1 MLTK (O2 MLTK K0)''')
    )
    rules.append(KET_MLT_9)


    KET_MLT_10 = CanonicalRule(
        "KET-MLT-10",
        lhs = parse(r'''(O1 TSRO O2) MLTK ((O1p TSRO O2p) MLTK K0)'''),
        rhs = parse(r'''((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTK K0''')
    )
    rules.append(KET_MLT_10)

    KET_MLT_11 = CanonicalRule(
        "KET-MLT-11",
        lhs = parse(r'''(O1 TSRO O2) MLTK KET(t)'''),
        rhs = parse(r'''(O1 MLTK KET(FST(t))) TSRK (O2 MLTK KET(SND(t)))''')
    )
    rules.append(KET_MLT_11)

    KET_MLT_12 = CanonicalRule(
        "KET-MLT-12",
        lhs = parse(r'''(O1 TSRO O2) MLTK (K1 TSRK K2)'''),
        rhs = parse(r'''(O1 MLTK K1) TSRK (O2 MLTK K2)''')
    )
    rules.append(KET_MLT_12)

    KET_TSR_1 = CanonicalRule(
        "KET-TSR-1",
        lhs = parse(r'''0X TSRK K0'''),
        rhs = parse(r'''0X''')
    )
    rules.append(KET_TSR_1)

    KET_TSR_2 = CanonicalRule(
        "KET-TSR-2",
        lhs = parse(r'''K0 TSRK 0X'''),
        rhs = parse(r'''0X''')
    )
    rules.append(KET_TSR_2)

    KET_TSR_3 = CanonicalRule(
        "KET-TSR-3",
        lhs = parse(r'''KET(s) TSRK KET(t)'''),
        rhs = parse(r'''KET(PAIR(s, t))''')
    )
    rules.append(KET_TSR_3)

    KET_TSR_4 = CanonicalRule(
        "KET-TSR-4",
        lhs = parse(r'''(S0 SCR K1) TSRK K2'''),
        rhs = parse(r'''S0 SCR (K1 TSRK K2)''')
    )
    rules.append(KET_TSR_4)

    KET_TSR_5 = CanonicalRule(
        "KET-TSR-5",
        lhs = parse(r'''K1 TSRK (S0 SCR K2)'''),
        rhs = parse(r'''S0 SCR (K1 TSRK K2)''')
    )
    rules.append(KET_TSR_5)


    KET_TSR_6 = CanonicalRule(
        "KET-TSR-6",
        lhs = parse("(K1 ADD K2) TSRK K0"),
        rhs = parse("(K1 TSRK K0) ADD (K2 TSRK K0)")
    )
    rules.append(KET_TSR_6)


    KET_TSR_7 = CanonicalRule(
        "KET-TSR-7",
        lhs = parse("K0 TSRK (K1 ADD K2)"),
        rhs = parse("(K0 TSRK K1) ADD (K0 TSRK K2)")
    )
    rules.append(KET_TSR_7)


    ###################################################
    # Bra

    BRA_MLT_1 = CanonicalRule(
        "BRA-MLT-1",
        lhs = parse(r'''B0 MLTB 0X'''),
        rhs = parse(r'''0X''')
    )
    rules.append(BRA_MLT_1)

    BRA_MLT_2 = CanonicalRule(
        "BRA-MLT-2",
        lhs = parse(r'''0X MLTB O0'''),
        rhs = parse(r'''0X''')
    )
    rules.append(BRA_MLT_2)

    BRA_MLT_3 = CanonicalRule(
        "BRA-MLT-3",
        lhs = parse(r'''B0 MLTB 1O'''),
        rhs = parse(r'''B0''')
    )
    rules.append(BRA_MLT_3)

    BRA_MLT_4 = CanonicalRule(
        "BRA-MLT-4",
        lhs = parse(r'''B0 MLTB (S0 SCR O0)'''),
        rhs = parse(r'''S0 SCR (B0 MLTB O0)''')
    )
    rules.append(BRA_MLT_4)

    BRA_MLT_5 = CanonicalRule(
        "BRA-MLT-5",
        lhs = parse(r'''(S0 SCR B0) MLTB O0'''),
        rhs = parse(r'''S0 SCR (B0 MLTB O0)''')
    )
    rules.append(BRA_MLT_5)


    BRA_MLT_6 = CanonicalRule(
        "BRA-MLT-6",
        lhs = parse("B0 MLTB (O1 ADD O2)"),
        rhs = parse("(B0 MLTB O1) ADD (B0 MLTB O2)")
    )
    rules.append(BRA_MLT_6)


    BRA_MLT_7 = CanonicalRule(
        "BRA-MLT-7",
        lhs = parse("(B1 ADD B2) MLTB O0"),
        rhs = parse("(B1 MLTB O0) ADD (B2 MLTB O0)")
    )
    rules.append(BRA_MLT_7)


    BRA_MLT_8 = CanonicalRule(
        "BRA-MLT-8",
        lhs = parse(r'''B1 MLTB (K1 OUTER B2)'''),
        rhs = parse(r'''(B1 DOT K1) SCR B2''')
    )
    rules.append(BRA_MLT_8)

    BRA_MLT_9 = CanonicalRule(
        "BRA-MLT-9",
        lhs = parse(r'''B0 MLTB (O1 MLTO O2)'''),
        rhs = parse(r'''(B0 MLTB O1) MLTB O2''')
    )
    rules.append(BRA_MLT_9)


    BRA_MLT_10 = CanonicalRule(
        "BRA-MLT-10",
        lhs = parse(r'''(B0 MLTB (O1 TSRO O2)) MLTB (O1p TSRO O2p)'''),
        rhs = parse(r'''B0 MLTB ((O1 MLTO O1p) TSRO (O2 MLTO O2p))''')
    )
    rules.append(BRA_MLT_10)

    BRA_MLT_11 = CanonicalRule(
        "BRA-MLT-11",
        lhs = parse(r'''BRA(t) MLTB (O1 TSRO O2)'''),
        rhs = parse(r'''(BRA(FST(t)) MLTB O1) TSRB (BRA(SND(t)) MLTB O2)''')
    )
    rules.append(BRA_MLT_11)

    BRA_MLT_12 = CanonicalRule(
        "BRA-MLT-12",
        lhs = parse(r'''(B1 TSRB B2) MLTB (O1 TSRO O2)'''),
        rhs = parse(r'''(B1 MLTB O1) TSRB (B2 MLTB O2)''')
    )
    rules.append(BRA_MLT_12)



    BRA_TSR_1 = CanonicalRule(
        "BRA-TSR-1",
        lhs = parse(r'''0X TSRB B0'''),
        rhs = parse(r'''0X''')
    )
    rules.append(BRA_TSR_1)

    BRA_TSR_2 = CanonicalRule(
        "BRA-TSR-2",
        lhs = parse(r'''B0 TSRB 0X'''),
        rhs = parse(r'''0X''')
    )
    rules.append(BRA_TSR_2)

    BRA_TSR_3 = CanonicalRule(
        "BRA-TSR-3",
        lhs = parse(r'''BRA(s) TSRB BRA(t)'''),
        rhs = parse(r'''BRA(PAIR(s, t))''')
    )
    rules.append(BRA_TSR_3)

    BRA_TSR_4 = CanonicalRule(
        "BRA-TSR-4",
        lhs = parse(r'''(S0 SCR B1) TSRB B2'''),
        rhs = parse(r'''S0 SCR (B1 TSRB B2)''')
    )
    rules.append(BRA_TSR_4)

    BRA_TSR_5 = CanonicalRule(
        "BRA-TSR-5",
        lhs = parse(r'''B1 TSRB (S0 SCR B2)'''),
        rhs = parse(r'''S0 SCR (B1 TSRB B2)''')
    )
    rules.append(BRA_TSR_5)

    BRA_TSR_6 = CanonicalRule(
        "BRA-TSR-6",
        lhs = parse("(B1 ADD B2) TSRB B0"),
        rhs = parse("(B1 TSRB B0) ADD (B2 TSRB B0)")
    )
    rules.append(BRA_TSR_6)

    BRA_TSR_7 = CanonicalRule(
        "BRA-TSR-7",
        lhs = parse("B0 TSRB (B1 ADD B2)"),
        rhs = parse("(B0 TSRB B1) ADD (B0 TSRB B2)")
    )
    rules.append(BRA_TSR_7)


    ###########################################################
    # Operators

    OPT_OUTER_1 = CanonicalRule(
        "OPT-OUTER-1",
        lhs = parse(r'''0X OUTER B0 '''),
        rhs = parse(r'''0X''')
    )
    rules.append(OPT_OUTER_1)

    OPT_OUTER_2 = CanonicalRule(
        "OPT-OUTER-2",
        lhs = parse(r'''K0 OUTER 0X'''),
        rhs = parse(r'''0X''')
    )
    rules.append(OPT_OUTER_2)

    OPT_OUTER_3 = CanonicalRule(
        "OPT-OUTER-3",
        lhs = parse(r'''(S0 SCR K0) OUTER B0'''),
        rhs = parse(r'''S0 SCR (K0 OUTER B0)''')
    )
    rules.append(OPT_OUTER_3)

    OPT_OUTER_4 = CanonicalRule(
        "OPT-OUTER-4",
        lhs = parse(r'''K0 OUTER (S0 SCR B0)'''),
        rhs = parse(r'''S0 SCR (K0 OUTER B0)''')
    )
    rules.append(OPT_OUTER_4)


    OPT_OUTER_5 = CanonicalRule(
        "OPT-OUTER-5",
        lhs = parse("(K1 ADD K2) OUTER B0"),
        rhs = parse("(K1 OUTER B0) ADD (K2 OUTER B0)")
    )
    rules.append(OPT_OUTER_5)

    OPT_OUTER_6 = CanonicalRule(
        "OPT-OUTER-6",
        lhs = parse("K0 OUTER (B1 ADD B2)"),
        rhs = parse("(K0 OUTER B1) ADD (K0 OUTER B2)")
    )
    rules.append(OPT_OUTER_6)


    OPT_MLT_1 = CanonicalRule(
        "OPT-MLT-1",
        lhs = parse(r'''0X MLTO O0'''),
        rhs = parse(r'''0X''')
    )
    rules.append(OPT_MLT_1)

    OPT_MLT_2 = CanonicalRule(
        "OPT-MLT-2",
        lhs = parse(r'''O0 MLTO 0X'''),
        rhs = parse(r'''0X''')
    )
    rules.append(OPT_MLT_2)

    OPT_MLT_3 = CanonicalRule(
        "OPT-MLT-3",
        lhs = parse(r'''1O MLTO O0'''),
        rhs = parse(r'''O0''')
    )
    rules.append(OPT_MLT_3)

    OPT_MLT_4 = CanonicalRule(
        "OPT-MLT-4",
        lhs = parse(r'''O0 MLTO 1O'''),
        rhs = parse(r'''O0''')
    )
    rules.append(OPT_MLT_4)

    OPT_MLT_5 = CanonicalRule(
        "OPT-MLT-5",
        lhs = parse(r'''(K0 OUTER B0) MLTO O0'''),
        rhs = parse(r'''K0 OUTER (B0 MLTB O0)''')
    )
    rules.append(OPT_MLT_5)

    OPT_MLT_6 = CanonicalRule(
        "OPT-MLT-6",
        lhs = parse(r'''O0 MLTO (K0 OUTER B0)'''),
        rhs = parse(r'''(O0 MLTK K0) OUTER B0''')
    )
    rules.append(OPT_MLT_6)

    OPT_MLT_7 = CanonicalRule(
        "OPT-MLT-7",
        lhs = parse(r'''(S0 SCR O1) MLTO O2'''),
        rhs = parse(r'''S0 SCR (O1 MLTO O2)''')
    )
    rules.append(OPT_MLT_7)

    OPT_MLT_8 = CanonicalRule(
        "OPT-MLT-8",
        lhs = parse(r'''O1 MLTO (S0 SCR O2)'''),
        rhs = parse(r'''S0 SCR (O1 MLTO O2)''')
    )
    rules.append(OPT_MLT_8)

    def opt_mlt_9_rewrite(rule, trs, term):
        if isinstance(term, OpApply) and isinstance(term.args[0], Add):
            new_args = tuple(OpApply(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    OPT_MLT_9 = Rule(
        "OPT-MLT-9",
        lhs = "(O1 ADD O2) MLTO O0",
        rhs = "(O1 MLTO O0) ADD (O2 MLTO O0)",
        rewrite_method=opt_mlt_9_rewrite
    )
    rules.append(OPT_MLT_9)

    def opt_mlt_10_rewrite(rule, trs, term):
        if isinstance(term, OpApply) and isinstance(term.args[1], Add):
            new_args = tuple(OpApply(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    OPT_MLT_10 = Rule(
        "OPT-MLT-10",
        lhs = "O0 MLTO (O1 ADD O2)",
        rhs = "(O0 MLTO O1) ADD (O0 MLTO O2)",
        rewrite_method=opt_mlt_10_rewrite
    )
    rules.append(OPT_MLT_10)

    OPT_MLT_11 = CanonicalRule(
        "OPT-MLT-11",
        lhs = parse(r'''(O1 MLTO O2) MLTO O3'''),
        rhs = parse(r'''O1 MLTO (O2 MLTO O3)''')
    )
    rules.append(OPT_MLT_11)

    OPT_MLT_12 = CanonicalRule(
        "OPT-MLT-12",
        lhs = parse(r'''(O1 TSRO O2) MLTO (O1p TSRO O2p)'''),
        rhs = parse(r'''(O1 MLTO O1p) TSRO (O2 MLTO O2p)''')
    )
    rules.append(OPT_MLT_12)

    OPT_MLT_13 = CanonicalRule(
        "OPT-MLT-13",
        lhs = parse(r'''(O1 TSRO O2) MLTO ((O1p TSRO O2p) MLTO O3)'''),
        rhs = parse(r'''((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTO O3''')
    )
    rules.append(OPT_MLT_13)


    OPT_TSR_1 = CanonicalRule(
        "OPT-TSR-1",
        lhs = parse(r'''0X TSRO O0'''),
        rhs = parse(r'''0X''')
    )
    rules.append(OPT_TSR_1)

    OPT_TSR_2 = CanonicalRule(
        "OPT-TSR-2",
        lhs = parse(r'''O0 TSRO 0X'''),
        rhs = parse(r'''0X''')
    )
    rules.append(OPT_TSR_2)

    OPT_TSR_3 = CanonicalRule(
        "OPT-TSR-3",
        lhs = parse(r''' 1O TSRO 1O '''),
        rhs = parse(r''' 1O ''')
    )
    rules.append(OPT_TSR_3)

    OPT_TSR_4 = CanonicalRule(
        "OPT-TSR-4",
        lhs = parse(r'''(K1 OUTER B1) TSRO (K2 OUTER B2)'''),
        rhs = parse(r'''(K1 TSRK K2) OUTER (B1 TSRB B2)''')
    )
    rules.append(OPT_TSR_4)

    OPT_TSR_5 = CanonicalRule(
        "OPT-TSR-5",
        lhs = parse(r'''(S0 SCR O1) TSRO O2'''),
        rhs = parse(r'''S0 SCR (O1 TSRO O2)''')
    )
    rules.append(OPT_TSR_5)

    OPT_TSR_6 = CanonicalRule(
        "OPT-TSR-6",
        lhs = parse(r'''O1 TSRO (S0 SCR O2)'''),
        rhs = parse(r'''S0 SCR (O1 TSRO O2)''')
    )
    rules.append(OPT_TSR_6)

    def opt_tsr_7_rewrite(rule, trs, term):
        if isinstance(term, OpTensor) and isinstance(term.args[0], Add):
            new_args = tuple(OpTensor(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    OPT_TSR_7 = Rule(
        "OPT-TSR-7",
        lhs = "(O1 ADD O2) TSRO O0",
        rhs = "(O1 TSRO O0) ADD (O2 TSRO O0)",
        rewrite_method=opt_tsr_7_rewrite
    )
    rules.append(OPT_TSR_7)

    def opt_tsr_8_rewrite(rule, trs, term):
        if isinstance(term, OpTensor) and isinstance(term.args[1], Add):
            new_args = tuple(OpTensor(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    OPT_TSR_8 = Rule(
        "OPT-TSR-8",
        lhs = "O0 TSRO (O1 ADD O2)",
        rhs = "(O0 TSRO O1) ADD (O0 TSRO O2)",
        rewrite_method=opt_tsr_8_rewrite
    )
    rules.append(OPT_TSR_8)



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
  0X_S : unary ;
  KET_S : unary ;
  ADJ_S : unary ;
  SCR_S : infix binary ;
  ADD_S : infix binary ;
  MLTK_S : infix binary ;
  TSRK_S : infix binary ;

  (* Bra *)
  0X_S : unary ;
  BRA_S : unary ;
  ADJ_S : unary ;
  SCR_S : infix binary ;
  ADD_S : infix binary ;
  MLTB_S : infix binary ;
  TSRB_S : infix binary ;

  (* Operator *)
  0X_S : binary ;
  1O_S : unary ;
  OUTER_S : infix binary ;
  ADJ_S : unary ;
  SCR_S : infix binary ;
  ADD_S : infix binary ;
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
  0X : constant ;
  KET : unary ;
  ADJ : unary ;
  SCR : infix binary ;
  ADD : AC ;
  MLTK : infix binary ;
  TSRK : infix binary ;

  (* Bra *)
  0X : constant ;
  BRA : unary ;
  ADJ : unary ;
  SCR : infix binary ;
  ADD : AC ;
  MLTB : infix binary ;
  TSRB : infix binary ;

  (* Operator *)
  0X : constant ;
  1O : constant ;
  OUTER : infix binary ;
  ADJ : unary ;
  SCR : infix binary ;
  ADD : AC ;
  MLTO : infix binary ;
  TSRO : infix binary ;

";

let X = vars "a b c x S0 S1 S2 S3 s s1 s2 t t1 t2 B0 B1 B2 K0 K1 K2 O0 O1 O2 O1' O2' T1 T2 T3 T4 O1p O2p O3";

let R = TRS F X "

  (* ######################## TYPE CHECKING ############################ *)
  C_S(a) -> S(C(a)) ;
  DELTA_S(Base(s, T1), Base(t, T1)) -> S(DELTA(s, t)) ;
  S(a) ADDS_S S(b) -> S(a ADDS b) ;
  S(a) MLTS_S S(b) -> S(a MLTS b) ;
  CONJS_S(S(a)) -> S(CONJS(a)) ;
  B(B0, T1) DOT_S K(K0, T1) -> S(B0 DOT K0) ;

  (* Ket *)
  0X_S(T1) -> K(0X, T1) ;
  KET_S(Base(s, T1)) -> K(KET(s), T1) ;
  ADJ_S(B(B0, T1)) -> K(ADJ(B0), T1) ;
  S(S0) SCR_S K(K0, T1) -> K(S0 SCR K0, T1) ;
  K(K1, T1) ADD_S K(K2, T1) -> K(K1 ADD K2, T1) ;
  O(O0, T1, T2) MLTK_S K(K0, T2) -> K(O0 MLTK K0, T1) ;
  K(K1, T1) TSRK_S K(K2, T2) -> K(K1 TSRK K2, T1 PROD T2) ;

  (* Bra *)
  0X_S(T1) -> B(0X, T1) ;
  BRA_S(Base(s, T1)) -> B(BRA(s), T1) ;
  ADJ_S(K(K0, T1)) -> B(ADJ(K0), T1) ;
  S(S0) SCR_S B(B0, T1) -> B(S0 SCR B0, T1) ;
  B(B1, T1) ADD_S B(B2, T1) -> B(B1 ADD B2, T1) ;
  B(B0, T1) MLTB_S O(O0, T1, T2) -> B(B0 MLTB O0, T2) ;
  B(B1, T1) TSRB_S B(B2, T2) -> B(B1 TSRB B2, T1 PROD T2) ;

  (* Operator *)
  0X_S(T1, T2) -> O(0X, T1, T2) ;
  1O_S(T1) -> O(1O, T1, T1) ;
  K(K0, T1) OUTER_S B(B0, T2) -> O(K0 OUTER B0, T1, T2) ;
  ADJ_S(O(O0, T1, T2)) -> O(ADJ(O0), T2, T1) ;
  S(S0) SCR_S O(O0, T1, T2) -> O(S0 SCR O0, T1, T2) ;
  O(O1, T1, T2) ADD_S O(O2, T1, T2) -> O(O1 ADD O2, T1, T2) ;
  O(O1, T1, T2) MLTO_S O(O2, T2, T3) -> O(O1 MLTO O2, T1, T3) ;
  O(O1, T1, T2) TSRO_S O(O2, T3, T4) -> O(O1 TSRO O2, T1 PROD T3, T2 PROD T4) ;

  (* -------- overload the universal application --------- *)
  S(S1) @ S(S2) -> S(S1 MLTS S2) ;
  S(S0) @ K(K0, T1) -> K(S0 SCR K0, T1) ;
  S(S0) @ B(B0, T1) -> B(S0 SCR B0, T1) ;

  S(S0) @ O(O0, T1, T2) -> O(S0 SCR O0, T1, T2) ;
  K(K0, T1) @ S(S0) -> K(S0 SCR K0, T1) ;
  K(K1, T1) @ K(K2, T2) -> K(K1 TSRK K2, T1 PROD T2) ;
  K(K0, T1) @ B(B0, T2) -> O(K0 OUTER B0, T1, T2) ;

  B(B0, T1) @ S(S0) -> B(S0 SCR B0, T1) ;
  B(B0, T1) @ K(K0, T1) -> S(B0 DOT K0) ;
  B(B1, T1) @ B(B2, T2) -> B(B1 TSRB B2, T1 PROD T2) ;
  B(B0, T1) @ O(O0, T1, T2) -> B(B0 MLTB O0, T2) ;

  O(O0, T1, T2) @ S(S0) -> O(S0 SCR O0, T1, T2) ;
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

  (K0 ADD 0X) ADD x -> K0 ADD x ;
  (K0 ADD K0) ADD x -> (C(1 + 1) SCR K0) ADD x ;
  ((S0 SCR K0) ADD K0) ADD x -> ((S0 ADDS C(1)) SCR K0) ADD x ;
  ((S1 SCR K0) ADD (S2 SCR K0)) ADD x -> ((S1 ADDS S2) SCR K0) ADD x ;

  (B0 ADD 0X) ADD x -> B0 ADD x ;
  (B0 ADD B0) ADD x -> (C(1 + 1) SCR B0) ADD x ;
  ((S0 SCR B0) ADD B0) ADD x -> ((S0 ADDS C(1)) SCR B0) ADD x ;
  ((S1 SCR B0) ADD (S2 SCR B0)) ADD x -> ((S1 ADDS S2) SCR B0) ADD x ;

  (O0 ADD 0X) ADD x -> O0 ADD x ;
  (O0 ADD O0) ADD x -> (C(1 + 1) SCR O0) ADD x ;
  ((S0 SCR O0) ADD O0) ADD x -> ((S0 ADDS C(1)) SCR O0) ADD x ;
  ((S1 SCR O0) ADD (S2 SCR O0)) ADD x -> ((S1 ADDS S2) SCR O0) ADD x ;
  
";

(* optional : 

  DELTA(s, s) -> C(1) ;

*)
'''
    with open(path, "w") as p:
        p.write(code)