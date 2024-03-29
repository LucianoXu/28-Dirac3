
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
        parse: Callable[[str], Any]) -> TRS:

    trs = TRS([])


    C0 = CScalar.zero()
    C1 = CScalar.one()
    C2 = CScalar.add(CScalar.one(), CScalar.one())

    
    #################################################
    # reducing basis and complex scalars

    def atomic_base_rewrite(rule, trs, term):
        if isinstance(term, ABase):
            return term.reduce()
    trs.append(Rule(
        "ATOMIC-BASE",
        lhs = "a",
        rhs = "a",
        rewrite_method=atomic_base_rewrite,
        rule_repr="(* base -> simp(base) *)"
    ))

    def complex_scalar_rewrite(rule, trs, term):
        if isinstance(term, CScalar):
            return term.reduce()
    trs.append(Rule(
        "COMPLEX-SCALAR",
        lhs = "a",
        rhs = "a",
        rewrite_method=complex_scalar_rewrite,
        rule_repr="(* complex -> simp(complex) *)"
    ))


    #################################################
    # Base
    trs.append(CanonicalRule(
        "BASIS-1",
        lhs = parse("FST(PAIR(s, t))"),
        rhs = parse("s")
    ))

    trs.append(CanonicalRule(
        "BASIS-2",
        lhs = parse("SND(PAIR(s, t))"),
        rhs = parse("t")
    ))

    trs.append(CanonicalRule(
        "BASIS-3",
        lhs = parse("PAIR(FST(s), SND(s))"),
        rhs = parse("s")
    ))

    #################################################
    # Delta
    def delta_1_rewrite(rule, trs, term):
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
    trs.append(Rule(
        "DELTA-1",
        lhs = "DELTA(s, PAIR(t1, t2))",
        rhs = "DELTA(FST(s), t1) MLTS DELTA(SND(s), t2)",
        rewrite_method=delta_1_rewrite
    ))


    def delta_2_rewrite(rule, trs, term):
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
                            and isinstance(term.args[j].args[1], BaseSnd) \
                            and term.args[i].args[0].args[0] == term.args[j].args[0].args[0] \
                            and term.args[i].args[1].args[0] == term.args[j].args[1].args[0]:

                            deltauv = ScalarDelta(term.args[i].args[0].args[0], term.args[i].args[1].args[0])

                            return ScalarMlt(deltauv, *term.remained_terms(i, j))
    trs.append(Rule(
        "DELTA-2",
        lhs = "DELTA(FST(s), FST(t)) MLTS DELTA(SND(s), SND(t))",
        rhs = "DELTA(s, t)",
        rewrite_method=delta_2_rewrite
    ))
    
    #################################################
    # Scalar

    def scr_cop_1_rewrite(rule, trs, term):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                if term.args[i] == C0:
                    return ScalarAdd(*term.remained_terms(i))

    trs.append(Rule(
        "SCR-COP-1",
        lhs="C(0) ADDS a", 
        rhs="a",
        rewrite_method=scr_cop_1_rewrite
    ))


    def scr_cop_2_rewrite(rule, trs, term):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ComplexScalar):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], ComplexScalar):

                            new_args = (CScalar.add(term.args[i], term.args[j]),) + term.remained_terms(i, j)

                            return ScalarAdd(*new_args)

    trs.append(Rule(
        "SCR-COP-2",
        lhs="C(a) ADDS C(b)", 
        rhs="C(a + b)",
        rewrite_method=scr_cop_2_rewrite
    ))

    def scr_cop_3_rewrite(rule, trs, term):
        if isinstance(term, ScalarAdd):
            for i in range(len(term.args)):
                for j in range(i+1, len(term.args)):
                    if term.args[i] == term.args[j]:
                        new_args = (ScalarMlt(C2, term.args[i]),) + term.remained_terms(i, j)
                        return ScalarAdd(*new_args)
                    
    trs.append(Rule(
        "SCR-COP-3",
        lhs = "S0 ADDS S0",
        rhs = "C(1 + 1) MLTS S0",
        rewrite_method=scr_cop_3_rewrite
    ))

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
                                
    trs.append(Rule(
        "SCR-COP-4",
        lhs = "(C(a) MLTS S0) ADDS S0",
        rhs = "C(a + 1) MLTS S0",
        rewrite_method=scr_cop_4_rewrite
    ))

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

    trs.append(Rule(
        "SCR-COP-5",
        lhs = "(C(a) MLTS S0) ADDS (C(b) MLTS S0)",
        rhs = "C(a + b) MLTS S0",
        rewrite_method=scr_cop_5_rewrite
    ))

    def scr_cop_6_rewrite(rule, trs, term):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if term.args[i] == C0:
                    return C0
    trs.append(Rule(
        "SCR-COP-6",
        lhs="C(0) MLTS a", 
        rhs="C(0)",
        rewrite_method=scr_cop_6_rewrite
    ))

    def scr_cop_7_rewrite(rule, trs, term):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if term.args[i] == C1:
                    return ScalarMlt(*term.remained_terms(i))
    trs.append(Rule(
        "SCR-COP-7",
        lhs="C(1) MLTS a", 
        rhs="a",
        rewrite_method=scr_cop_7_rewrite
    ))


    def scr_cop_8_rewrite(rule, trs, term):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ComplexScalar):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], ComplexScalar):

                            new_args = (CScalar.mlt(term.args[i], term.args[j]),) + term.remained_terms(i, j)

                            return ScalarMlt(*new_args)

    trs.append(Rule(
        "SCR-COP-8",
        lhs="C(a) MLTS C(b)",
        rhs="C(a * b)",
        rewrite_method=scr_cop_8_rewrite
    ))

    def scr_cop_9_rewrite(rule, trs, term):
        if isinstance(term, ScalarMlt):
            for i in range(len(term.args)):
                if isinstance(term.args[i], ScalarAdd):
                    S1 = ScalarMlt(*term.args[:i], *term.args[i+1:])
                    new_args = tuple(ScalarMlt(S1, term.args[i][j]) for j in range(len(term.args[i].args)))
                    return ScalarAdd(*new_args)
    trs.append(Rule(
        "SCR-COP-9",
        lhs="a MLTS (b ADDS c)",
        rhs="(a MLTS b) ADDS (a MLTS c)",
        rewrite_method=scr_cop_9_rewrite
    ))


    def scr_cop_10_rewrite(rule, trs, term):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ComplexScalar):
                return CScalar.conj(term.args[0])
    trs.append(Rule(
        "SCR-COP-10",
        lhs="CONJS(C(a))",
        rhs="C(a ^*)",
        rewrite_method=scr_cop_10_rewrite
    ))
        

    def scr_cop_11_rewrite(rule, trs, term):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ScalarDelta):
                return term.args[0]
            
    trs.append(Rule(
        "SCR-COP-11",
        lhs="CONJS(DELTA(a, b))",
        rhs="DELTA(a, b)",
        rewrite_method=scr_cop_11_rewrite
    ))


    def scr_cop_12_rewrite(rule, trs, term):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ScalarAdd):
                new_args = tuple(ScalarConj(arg) for arg in term.args[0].args)
                return ScalarAdd(*new_args)
    trs.append(Rule(
        "SCR-COP-12",
        lhs="CONJS(a ADDS b)",
        rhs="CONJS(a) ADDS CONJS(b)",
        rewrite_method=scr_cop_12_rewrite
    ))


    def scr_cop_13_rewrite(rule, trs, term):
        if isinstance(term, ScalarConj):
            if isinstance(term.args[0], ScalarMlt):
                new_args = tuple(ScalarConj(arg) for arg in term.args[0].args)
                return ScalarMlt(*new_args)
    trs.append(Rule(
        "SCR-COP-13",
        lhs="CONJS(a MLTS b)",
        rhs="CONJS(a) MLTS CONJS(b)",
        rewrite_method=scr_cop_13_rewrite
    ))


    trs.append(CanonicalRule(
        "SCR-COP-14",
        lhs=parse(r''' CONJS(CONJS(a)) '''), 
        rhs=parse(r''' a ''')
    ))

    trs.append(CanonicalRule(
        "SCR-COP-15",
        lhs = parse(r''' CONJS(B0 DOT K0) '''),
        rhs = parse(r''' ADJ(K0) DOT ADJ(B0) ''')
    ))


    trs.append(CanonicalRule(
        "SCR-DOT-1",
        lhs = parse(r''' 0X DOT K0 '''),
        rhs = parse(r''' "0" '''),
        rule_repr = '''0X DOT K0 -> C(0) ;'''
    ))

    trs.append(CanonicalRule(
        "SCR-DOT-2",
        lhs = parse(r''' B0 DOT 0X '''),
        rhs = parse(r''' "0" '''),
        rule_repr = '''B0 DOT 0X -> C(0) ;'''
    ))

    trs.append(CanonicalRule(
        "SCR-DOT-3",
        lhs = parse(r'''(S0 SCR B0) DOT K0'''),
        rhs = parse(r'''S0 MLTS (B0 DOT K0)''')
    ))


    trs.append(CanonicalRule(
        "SCR-DOT-4",
        lhs = parse(r'''B0 DOT (S0 SCR K0)'''),
        rhs = parse(r'''S0 MLTS (B0 DOT K0)''')
    ))

    def scr_dot_5_rewrite(rule, trs, term):
        if isinstance(term, ScalarDot):
            if isinstance(term.args[0], Add):
                new_args = tuple(ScalarDot(arg, term.args[1]) for arg in term.args[0].args)
                return ScalarAdd(*new_args)
    trs.append(Rule(
        "SCR-DOT-5",
        lhs = "(B1 ADD B2) DOT K0",
        rhs = "(B1 DOT K0) ADDS (B2 DOT K0)",
        rewrite_method=scr_dot_5_rewrite
    ))

    def scr_dot_6_rewrite(rule, trs, term):
        if isinstance(term, ScalarDot):
            if isinstance(term.args[1], Add):
                new_args = tuple(ScalarDot(term.args[0], arg) for arg in term.args[1].args)
                return ScalarAdd(*new_args)
    trs.append(Rule(
        "SCR-DOT-6",
        lhs = "B0 DOT (K1 ADD K2)",
        rhs = "(B0 DOT K1) ADDS (B0 DOT K2)",
        rewrite_method=scr_dot_6_rewrite
    ))


    trs.append(CanonicalRule(
        "SCR-DOT-7",
        lhs = parse(r''' BRA(s) DOT KET(t) '''),
        rhs = parse(r''' DELTA(s, t) ''')
    ))


    trs.append(CanonicalRule(
        "SCR-DOT-8",
        lhs = parse(r'''(B1 TSRB B2) DOT KET(t)'''),
        rhs = parse(r'''(B1 DOT KET(FST(t))) MLTS (B2 DOT KET(SND(t)))''')
    ))

            
    trs.append(CanonicalRule(
        "SCR-DOT-9",
        lhs = parse(r'''BRA(s) DOT (K1 TSRK K2)'''),
        rhs = parse(r'''(BRA(FST(s)) DOT K1) MLTS (BRA(SND(s)) DOT K2)''')
    ))

            
    trs.append(CanonicalRule(
        "SCR-DOT-10",
        lhs = parse(r'''(B1 TSRB B2) DOT (K1 TSRK K2)'''),
        rhs = parse(r'''(B1 DOT K1) MLTS (B2 DOT K2)'''),
    ))

    trs.append(CanonicalRule(
        "SCR-SORT-1",
        lhs = parse(r''' (B0 MLTB O0) DOT K0 '''),
        rhs = parse(r''' B0 DOT (O0 MLTK K0) ''')
    ))
    

    trs.append(CanonicalRule(
        "SCR-SORT-2",
        lhs = parse(r''' BRA(s) DOT ((O1 TSRO O2) MLTK K0) '''),
        rhs = parse(r''' ((BRA(FST(s)) MLTB O1) TSRB (BRA(SND(s)) MLTB O2)) DOT K0 ''')
    ))

    trs.append(CanonicalRule(
        "SCR-SORT-3",
        lhs = parse(r''' (B1 TSRB B2) DOT ((O1 TSRO O2) MLTK K0) '''),
        rhs = parse(r''' ((B1 MLTB O1) TSRB (B2 MLTB O2)) DOT K0''')
    ))


    #######################################
    # unified symbols

    trs.append(CanonicalRule(
        "ADJ-UNI-1",
        lhs = parse(r'''ADJ(0X)'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "ADJ-UNI-2",
        lhs = parse(r'''ADJ(ADJ(X0))'''),
        rhs = parse(r'''X0''')
    ))

    trs.append(CanonicalRule(
        "ADJ-UNI-3",
        lhs = parse(r'''ADJ(S0 SCR X0)'''),
        rhs = parse(r'''CONJS(S0) SCR ADJ(X0)'''),
    ))

    
    def adj_uni_4_rewrite(rule, trs, term):
        if isinstance(term, Adj):
            if isinstance(term.args[0], Add):
                new_args = tuple(Adj(arg) for arg in term.args[0].args)
                return Add(*new_args)
    trs.append(Rule(
        "ADJ-UNI-4",
        lhs = "ADJ(X1 ADD X2)",
        rhs = "ADJ(X1) ADD ADJ(X2)",
        rewrite_method=adj_uni_4_rewrite
    ))


    trs.append(CanonicalRule(
        "ADJ-KET-1",
        lhs = parse(r'''ADJ(BRA(s))'''),
        rhs = parse(r'''KET(s)''')
    ))

    trs.append(CanonicalRule(
        "ADJ-KET-2",
        lhs = parse(r'''ADJ(B0 MLTB O0)'''),
        rhs = parse(r'''ADJ(O0) MLTK ADJ(B0)''')
    ))

    trs.append(CanonicalRule(
        "ADJ-KET-3",
        lhs = parse(r''' ADJ(B1 TSRB B2) '''),
        rhs = parse(r''' ADJ(B1) TSRK ADJ(B2) ''')
    ))

    trs.append(CanonicalRule(
        "ADJ-BRA-1",
        lhs = parse(r'''ADJ(KET(s))'''),
        rhs = parse(r'''BRA(s)''')
    ))

    trs.append(CanonicalRule(
        "ADJ-BRA-2",
        lhs = parse(r'''ADJ(O0 MLTK K0)'''),
        rhs = parse(r'''ADJ(K0) MLTB ADJ(O0)''')
    ))

    trs.append(CanonicalRule(
        "ADJ-BRA-3",
        lhs = parse(r''' ADJ(K1 TSRK K2) '''),
        rhs = parse(r''' ADJ(K1) TSRB ADJ(K2) ''')
    ))


    trs.append(CanonicalRule(
        "ADJ-OPT-1",
        lhs = parse(r'''ADJ(1O)'''),
        rhs = parse(r'''1O''')
    ))

    trs.append(CanonicalRule(
        "ADJ-OPT-2",
        lhs = parse(r'''ADJ(K0 OUTER B0)'''),
        rhs = parse(r'''ADJ(B0) OUTER ADJ(K0)''')
    ))


    trs.append(CanonicalRule(
        "ADJ-OPT-3",
        lhs = parse(r'''ADJ(O1 MLTO O2)'''),
        rhs = parse(r'''ADJ(O2) MLTO ADJ(O1)''')
    ))


    trs.append(CanonicalRule(
        "ADJ-OPT-4",
        lhs = parse(r'''ADJ(O1 TSRO O2)'''),
        rhs = parse(r'''ADJ(O1) TSRO ADJ(O2)''')
    ))


    trs.append(CanonicalRule(
        "SCR-1",
        lhs = parse(r''' "0" SCR X0 '''),
        rhs = parse(r''' 0X '''),
        rule_repr = '''C(0) SCR X0 -> 0X ;'''
    ))


    trs.append(CanonicalRule(
        "SCR-2",
        lhs = parse(r''' "1" SCR X0 '''),
        rhs = parse(r''' X0 '''),
        rule_repr = '''C(1) SCR X0 -> X0 ;'''
    ))

    trs.append(CanonicalRule(
        "SCR-3",
        lhs = parse(r'''S0 SCR 0X'''),
        rhs = parse(r''' 0X ''')
    ))

        
    trs.append(CanonicalRule(
        "SCR-4",
        lhs = parse(r'''S1 SCR (S2 SCR X0)'''),
        rhs = parse(r'''(S1 MLTS S2) SCR X0'''),
    ))


    def scr_5_rewrite(rule, trs, term):
        if isinstance(term, Scal):
            if isinstance(term.args[1], Add):
                new_args = tuple(Scal(term.args[0], arg) for arg in term.args[1].args)
                return Add(*new_args)
            
    trs.append(Rule(
        "SCR-5",
        lhs = "S0 SCR (X1 ADD X2)",
        rhs = "(S0 SCR X1) ADD (S0 SCR X2)",
        rewrite_method=scr_5_rewrite
    ))


    def add_1_rewrite(rule, trs, term):
        if isinstance(term, Add):
            for i in range(len(term.args)):
                if term.args[i] == Zero():
                    return Add(*term.remained_terms(i))
    trs.append(Rule(
        "ADD-1",
        lhs = "0X ADD X0",
        rhs = "X0",
        rewrite_method=add_1_rewrite
    ))

    def add_2_rewrite(rule, trs, term):
        if isinstance(term, Add):
            for i in range(len(term.args)):
                for j in range(i+1, len(term.args)):
                    if term.args[i] == term.args[j]:
                        new_args = (Scal(C2, term.args[i]),) + term.remained_terms(i, j)
                        return Add(*new_args)
    trs.append(Rule(
        "ADD-2",
        lhs = "X0 ADD X0",
        rhs = "C(1 + 1) SCR X0",
        rewrite_method=add_2_rewrite
    ))

    def add_3_rewrite(rule, trs, term):
        if isinstance(term, Add):
            for i in range(len(term.args)):
                if isinstance(term.args[i], Scal):
                    for j in range(len(term.args)):
                        if term.args[i].args[1] == term.args[j]:
                            new_args = (
                                Scal(ScalarAdd(term.args[i].args[0], C1), term.args[j]),) + term.remained_terms(i, j)
                            return Add(*new_args)
    trs.append(Rule(
        "ADD-3",
        lhs = "(S0 SCR X0) ADD X0",
        rhs = "(S0 ADDS C(1)) SCR X0",
        rewrite_method=add_3_rewrite
    ))

    def add_4_rewrite(rule, trs, term):
        if isinstance(term, Add):
            for i in range(len(term.args)):
                if isinstance(term.args[i], Scal):
                    for j in range(i+1, len(term.args)):
                        if isinstance(term.args[j], Scal):
                            if term.args[i].args[1] == term.args[j].args[1]:
                                new_args = (Scal(ScalarAdd(term.args[i].args[0], term.args[j].args[0]), term.args[i].args[1]),) + term.remained_terms(i, j)
                                return Add(*new_args)
    trs.append(Rule(
        "ADD-4",
        lhs = "(S1 SCR X0) ADD (S2 SCR X0)",
        rhs = "(S1 ADDS S2) SCR X0",
        rewrite_method=add_4_rewrite
    ))


    #######################################
    # Ket


    trs.append(CanonicalRule(
        "KET-MLT-1",
        lhs = parse(r'''0X MLTK K0'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "KET-MLT-2",
        lhs = parse(r'''O0 MLTK 0X'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "KET-MLT-3",
        lhs = parse(r'''1O MLTK K0'''),
        rhs = parse(r'''K0''')
    ))

    trs.append(CanonicalRule(
        "KET-MLT-4",
        lhs = parse(r'''(S0 SCR O0) MLTK K0'''),
        rhs = parse(r'''S0 SCR (O0 MLTK K0)''')
    ))

    trs.append(CanonicalRule(
        "KET-MLT-5",
        lhs = parse(r'''O0 MLTK (S0 SCR K0)'''),
        rhs = parse(r'''S0 SCR (O0 MLTK K0)''')
    ))


    def ket_mlt_6_rewrite(rule, trs, term):
        if isinstance(term, KetApply) and isinstance(term.args[0], Add):
            new_args = tuple(KetApply(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    trs.append(Rule(
        "KET-MLT-6",
        lhs = "(O1 ADD O2) MLTK K0",
        rhs = "(O1 MLTK K0) ADD (O2 MLTK K0)",
        rewrite_method=ket_mlt_6_rewrite
    ))


    def ket_mlt_7_rewrite(rule, trs, term):
        if isinstance(term, KetApply) and isinstance(term.args[1], Add):
            new_args = tuple(KetApply(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    trs.append(Rule(
        "KET-MLT-7",
        lhs = "O0 MLTK (K1 ADD K2)",
        rhs = "(O0 MLTK K1) ADD (O0 MLTK K2)",
        rewrite_method=ket_mlt_7_rewrite
    ))

    trs.append(CanonicalRule(
        "KET-MLT-8",
        lhs = parse(r'''(K1 OUTER B0) MLTK K2'''),
        rhs = parse(r'''(B0 DOT K2) SCR K1''')
    ))

    trs.append(CanonicalRule(
        "KET-MLT-9",
        lhs = parse(r'''(O1 MLTO O2) MLTK K0'''),
        rhs = parse(r'''O1 MLTK (O2 MLTK K0)''')
    ))


    trs.append(CanonicalRule(
        "KET-MLT-10",
        lhs = parse(r'''(O1 TSRO O2) MLTK ((O1p TSRO O2p) MLTK K0)'''),
        rhs = parse(r'''((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTK K0''')
    ))

    trs.append(CanonicalRule(
        "KET-MLT-11",
        lhs = parse(r'''(O1 TSRO O2) MLTK KET(t)'''),
        rhs = parse(r'''(O1 MLTK KET(FST(t))) TSRK (O2 MLTK KET(SND(t)))''')
    ))

    trs.append(CanonicalRule(
        "KET-MLT-12",
        lhs = parse(r'''(O1 TSRO O2) MLTK (K1 TSRK K2)'''),
        rhs = parse(r'''(O1 MLTK K1) TSRK (O2 MLTK K2)''')
    ))

    trs.append(CanonicalRule(
        "KET-TSR-1",
        lhs = parse(r'''0X TSRK K0'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "KET-TSR-2",
        lhs = parse(r'''K0 TSRK 0X'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "KET-TSR-3",
        lhs = parse(r'''KET(s) TSRK KET(t)'''),
        rhs = parse(r'''KET(PAIR(s, t))''')
    ))

    trs.append(CanonicalRule(
        "KET-TSR-4",
        lhs = parse(r'''(S0 SCR K1) TSRK K2'''),
        rhs = parse(r'''S0 SCR (K1 TSRK K2)''')
    ))

    trs.append(CanonicalRule(
        "KET-TSR-5",
        lhs = parse(r'''K1 TSRK (S0 SCR K2)'''),
        rhs = parse(r'''S0 SCR (K1 TSRK K2)''')
    ))


    def ket_tsr_6_rewrite(rule, trs, term):
        if isinstance(term, KetTensor) and isinstance(term.args[0], Add):
            new_args = tuple(KetTensor(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    trs.append(Rule(
        "KET-TSR-6",
        lhs = "(K1 ADD K2) TSRK K0",
        rhs = "(K1 TSRK K0) ADD (K2 TSRK K0)",
        rewrite_method=ket_tsr_6_rewrite
    ))

    def ket_tsr_7_rewrite(rule, trs, term):
        if isinstance(term, KetTensor) and isinstance(term.args[1], Add):
            new_args = tuple(KetTensor(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    trs.append(Rule(
        "KET-TSR-7",
        lhs = "K0 TSRK (K1 ADD K2)",
        rhs = "(K0 TSRK K1) ADD (K0 TSRK K2)",
        rewrite_method=ket_tsr_7_rewrite
    ))


    ###################################################
    # Bra

    trs.append(CanonicalRule(
        "BRA-MLT-1",
        lhs = parse(r'''B0 MLTB 0X'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-2",
        lhs = parse(r'''0X MLTB O0'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-3",
        lhs = parse(r'''B0 MLTB 1O'''),
        rhs = parse(r'''B0''')
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-4",
        lhs = parse(r'''B0 MLTB (S0 SCR O0)'''),
        rhs = parse(r'''S0 SCR (B0 MLTB O0)''')
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-5",
        lhs = parse(r'''(S0 SCR B0) MLTB O0'''),
        rhs = parse(r'''S0 SCR (B0 MLTB O0)''')
    ))


    def bra_mlt_6_rewrite(rule, trs, term):
        if isinstance(term, BraApply) and isinstance(term.args[1], Add):
            new_args = tuple(BraApply(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    trs.append(Rule(
        "BRA-MLT-6",
        lhs = "B0 MLTB (O1 ADD O2)",
        rhs = "(B0 MLTB O1) ADD (B0 MLTB O2)",
        rewrite_method=bra_mlt_6_rewrite
    ))


    def bra_mlt_7_rewrite(rule, trs, term):
        if isinstance(term, BraApply) and isinstance(term.args[0], Add):
            new_args = tuple(BraApply(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    trs.append(Rule(
        "BRA-MLT-7",
        lhs = "(B1 ADD B2) MLTB O0",
        rhs = "(B1 MLTB O0) ADD (B2 MLTB O0)",
        rewrite_method=bra_mlt_7_rewrite
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-8",
        lhs = parse(r'''B1 MLTB (K1 OUTER B2)'''),
        rhs = parse(r'''(B1 DOT K1) SCR B2''')
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-9",
        lhs = parse(r'''B0 MLTB (O1 MLTO O2)'''),
        rhs = parse(r'''(B0 MLTB O1) MLTB O2''')
    ))


    trs.append(CanonicalRule(
        "BRA-MLT-10",
        lhs = parse(r'''(B0 MLTB (O1 TSRO O2)) MLTB (O1p TSRO O2p)'''),
        rhs = parse(r'''B0 MLTB ((O1 MLTO O1p) TSRO (O2 MLTO O2p))''')
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-11",
        lhs = parse(r'''BRA(t) MLTB (O1 TSRO O2)'''),
        rhs = parse(r'''(BRA(FST(t)) MLTB O1) TSRB (BRA(SND(t)) MLTB O2)''')
    ))

    trs.append(CanonicalRule(
        "BRA-MLT-12",
        lhs = parse(r'''(B1 TSRB B2) MLTB (O1 TSRO O2)'''),
        rhs = parse(r'''(B1 MLTB O1) TSRB (B2 MLTB O2)''')
    ))


    trs.append(CanonicalRule(
        "BRA-TSR-1",
        lhs = parse(r'''0X TSRB B0'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "BRA-TSR-2",
        lhs = parse(r'''B0 TSRB 0X'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "BRA-TSR-3",
        lhs = parse(r'''BRA(s) TSRB BRA(t)'''),
        rhs = parse(r'''BRA(PAIR(s, t))''')
    ))

    trs.append(CanonicalRule(
        "BRA-TSR-4",
        lhs = parse(r'''(S0 SCR B1) TSRB B2'''),
        rhs = parse(r'''S0 SCR (B1 TSRB B2)''')
    ))

    trs.append(CanonicalRule(
        "BRA-TSR-5",
        lhs = parse(r'''B1 TSRB (S0 SCR B2)'''),
        rhs = parse(r'''S0 SCR (B1 TSRB B2)''')
    ))

    def bra_tsr_6_rewrite(rule, trs, term):
        if isinstance(term, BraTensor) and isinstance(term.args[0], Add):
            new_args = tuple(BraTensor(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    trs.append(Rule(
        "BRA-TSR-6",
        lhs = "(B1 ADD B2) TSRB B0",
        rhs = "(B1 TSRB B0) ADD (B2 TSRB B0)",
        rewrite_method=bra_tsr_6_rewrite
    ))

    def bra_tsr_7_rewrite(rule, trs, term):
        if isinstance(term, BraTensor) and isinstance(term.args[1], Add):
            new_args = tuple(BraTensor(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    trs.append(Rule(
        "BRA-TSR-7",
        lhs = "B0 TSRB (B1 ADD B2)",
        rhs = "(B0 TSRB B1) ADD (B0 TSRB B2)",
        rewrite_method=bra_tsr_7_rewrite
    ))


    ###########################################################
    # Operators

    trs.append(CanonicalRule(
        "OPT-OUTER-1",
        lhs = parse(r'''0X OUTER B0 '''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "OPT-OUTER-2",
        lhs = parse(r'''K0 OUTER 0X'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "OPT-OUTER-3",
        lhs = parse(r'''(S0 SCR K0) OUTER B0'''),
        rhs = parse(r'''S0 SCR (K0 OUTER B0)''')
    ))

    trs.append(CanonicalRule(
        "OPT-OUTER-4",
        lhs = parse(r'''K0 OUTER (S0 SCR B0)'''),
        rhs = parse(r'''S0 SCR (K0 OUTER B0)''')
    ))

    def opt_outer_5_rewrite(rule, trs, term):
        if isinstance(term, OpOuter) and isinstance(term.args[0], Add):
            new_args = tuple(OpOuter(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    trs.append(Rule(
        "OPT-OUTER-5",
        lhs = "(K1 ADD K2) OUTER B0",
        rhs = "(K1 OUTER B0) ADD (K2 OUTER B0)",
        rewrite_method=opt_outer_5_rewrite
    ))

    def opt_outer_6_rewrite(rule, trs, term):
        if isinstance(term, OpOuter) and isinstance(term.args[1], Add):
            new_args = tuple(OpOuter(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    trs.append(Rule(
        "OPT-OUTER-6",
        lhs = "K0 OUTER (B1 ADD B2)",
        rhs = "(K0 OUTER B1) ADD (K0 OUTER B2)",
        rewrite_method=opt_outer_6_rewrite
    ))


    trs.append(CanonicalRule(
        "OPT-MLT-1",
        lhs = parse(r'''0X MLTO O0'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-2",
        lhs = parse(r'''O0 MLTO 0X'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-3",
        lhs = parse(r'''1O MLTO O0'''),
        rhs = parse(r'''O0''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-4",
        lhs = parse(r'''O0 MLTO 1O'''),
        rhs = parse(r'''O0''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-5",
        lhs = parse(r'''(K0 OUTER B0) MLTO O0'''),
        rhs = parse(r'''K0 OUTER (B0 MLTB O0)''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-6",
        lhs = parse(r'''O0 MLTO (K0 OUTER B0)'''),
        rhs = parse(r'''(O0 MLTK K0) OUTER B0''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-7",
        lhs = parse(r'''(S0 SCR O1) MLTO O2'''),
        rhs = parse(r'''S0 SCR (O1 MLTO O2)''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-8",
        lhs = parse(r'''O1 MLTO (S0 SCR O2)'''),
        rhs = parse(r'''S0 SCR (O1 MLTO O2)''')
    ))

    def opt_mlt_9_rewrite(rule, trs, term):
        if isinstance(term, OpApply) and isinstance(term.args[0], Add):
            new_args = tuple(OpApply(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    trs.append(Rule(
        "OPT-MLT-9",
        lhs = "(O1 ADD O2) MLTO O0",
        rhs = "(O1 MLTO O0) ADD (O2 MLTO O0)",
        rewrite_method=opt_mlt_9_rewrite
    ))

    def opt_mlt_10_rewrite(rule, trs, term):
        if isinstance(term, OpApply) and isinstance(term.args[1], Add):
            new_args = tuple(OpApply(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    trs.append(Rule(
        "OPT-MLT-10",
        lhs = "O0 MLTO (O1 ADD O2)",
        rhs = "(O0 MLTO O1) ADD (O0 MLTO O2)",
        rewrite_method=opt_mlt_10_rewrite
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-11",
        lhs = parse(r'''(O1 MLTO O2) MLTO O3'''),
        rhs = parse(r'''O1 MLTO (O2 MLTO O3)''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-12",
        lhs = parse(r'''(O1 TSRO O2) MLTO (O1p TSRO O2p)'''),
        rhs = parse(r'''(O1 MLTO O1p) TSRO (O2 MLTO O2p)''')
    ))

    trs.append(CanonicalRule(
        "OPT-MLT-13",
        lhs = parse(r'''(O1 TSRO O2) MLTO ((O1p TSRO O2p) MLTO O3)'''),
        rhs = parse(r'''((O1 MLTO O1p) TSRO (O2 MLTO O2p)) MLTO O3''')
    ))


    trs.append(CanonicalRule(
        "OPT-TSR-1",
        lhs = parse(r'''0X TSRO O0'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "OPT-TSR-2",
        lhs = parse(r'''O0 TSRO 0X'''),
        rhs = parse(r'''0X''')
    ))

    trs.append(CanonicalRule(
        "OPT-TSR-3",
        lhs = parse(r''' 1O TSRO 1O '''),
        rhs = parse(r''' 1O ''')
    ))

    trs.append(CanonicalRule(
        "OPT-TSR-4",
        lhs = parse(r'''(K1 OUTER B1) TSRO (K2 OUTER B2)'''),
        rhs = parse(r'''(K1 TSRK K2) OUTER (B1 TSRB B2)''')
    ))

    trs.append(CanonicalRule(
        "OPT-TSR-5",
        lhs = parse(r'''(S0 SCR O1) TSRO O2'''),
        rhs = parse(r'''S0 SCR (O1 TSRO O2)''')
    ))

    trs.append(CanonicalRule(
        "OPT-TSR-6",
        lhs = parse(r'''O1 TSRO (S0 SCR O2)'''),
        rhs = parse(r'''S0 SCR (O1 TSRO O2)''')
    ))

    def opt_tsr_7_rewrite(rule, trs, term):
        if isinstance(term, OpTensor) and isinstance(term.args[0], Add):
            new_args = tuple(OpTensor(arg, term[1]) for arg in term.args[0].args)
            return Add(*new_args)
    trs.append(Rule(
        "OPT-TSR-7",
        lhs = "(O1 ADD O2) TSRO O0",
        rhs = "(O1 TSRO O0) ADD (O2 TSRO O0)",
        rewrite_method=opt_tsr_7_rewrite
    ))

    def opt_tsr_8_rewrite(rule, trs, term):
        if isinstance(term, OpTensor) and isinstance(term.args[1], Add):
            new_args = tuple(OpTensor(term[0], arg) for arg in term.args[1].args)
            return Add(*new_args)
    trs.append(Rule(
        "OPT-TSR-8",
        lhs = "O0 TSRO (O1 ADD O2)",
        rhs = "(O0 TSRO O1) ADD (O0 TSRO O2)",
        rewrite_method=opt_tsr_8_rewrite
    ))


    trs.set_rule_seq(
        [
            'ATOMIC-BASE',
            'COMPLEX-SCALAR',
            'BASIS-1',
            'BASIS-2',
            'BASIS-3',
            'DELTA-1',
            'DELTA-2',
            'SCR-COP-1',
            'SCR-COP-2',
            'SCR-COP-3',
            'SCR-COP-4',
            'SCR-COP-5',
            'SCR-COP-6',
            'SCR-COP-7',
            'SCR-COP-8',
            'SCR-COP-9',
            'SCR-COP-10',
            'SCR-COP-11',
            'SCR-COP-12',
            'SCR-COP-13',
            'SCR-COP-14',
            'SCR-COP-15',
            'SCR-DOT-1',
            'SCR-DOT-2',
            'SCR-DOT-3',
            'SCR-DOT-4',
            'SCR-DOT-7',
            'SCR-DOT-8',
            'SCR-DOT-9',
            'SCR-DOT-10',
            'SCR-SORT-1',
            'SCR-SORT-2',
            'SCR-SORT-3',
            'ADJ-UNI-1',
            'ADJ-UNI-2',
            'ADJ-UNI-3',
            'ADJ-UNI-4',
            'ADJ-KET-1',
            'ADJ-KET-2',
            'ADJ-KET-3',
            'ADJ-BRA-1',
            'ADJ-BRA-2',
            'ADJ-BRA-3',
            'ADJ-OPT-1',
            'ADJ-OPT-2',
            'ADJ-OPT-3',
            'ADJ-OPT-4',
            'ADD-1',
            'ADD-2',
            'ADD-3',
            'ADD-4',
            'SCR-1',
            'SCR-2',
            'SCR-3',
            'SCR-4',
            'KET-MLT-1',
            'KET-MLT-2',
            'KET-MLT-3',
            'KET-MLT-4',
            'KET-MLT-5',
            'KET-MLT-8',
            'KET-MLT-9',
            'KET-MLT-10',
            'KET-MLT-11',
            'KET-MLT-12',
            'KET-TSR-1',
            'KET-TSR-2',
            'KET-TSR-3',
            'KET-TSR-4',
            'KET-TSR-5',
            'BRA-MLT-1',
            'BRA-MLT-2',
            'BRA-MLT-3',
            'BRA-MLT-4',
            'BRA-MLT-5',
            'BRA-MLT-8',
            'BRA-MLT-9',
            'BRA-MLT-10',
            'BRA-MLT-11',
            'BRA-MLT-12',
            'BRA-TSR-1',
            'BRA-TSR-2',
            'BRA-TSR-3',
            'BRA-TSR-4',
            'BRA-TSR-5',
            'OPT-OUTER-1',
            'OPT-OUTER-2',
            'OPT-OUTER-3',
            'OPT-OUTER-4',
            'OPT-MLT-1',
            'OPT-MLT-2',
            'OPT-MLT-3',
            'OPT-MLT-4',
            'OPT-MLT-5',
            'OPT-MLT-6',
            'OPT-MLT-7',
            'OPT-MLT-8',
            'OPT-MLT-11',
            'OPT-MLT-12',
            'OPT-MLT-13',
            'OPT-TSR-1',
            'OPT-TSR-2',
            'OPT-TSR-3',
            'OPT-TSR-4',
            'OPT-TSR-5',
            'OPT-TSR-6',

            # expansion in the last stage
            'SCR-DOT-5',
            'SCR-DOT-6',
            'SCR-5',

            'KET-MLT-6',
            'KET-MLT-7',
            'BRA-MLT-6',
            'BRA-MLT-7',
            'OPT-MLT-9',
            'OPT-MLT-10',

            'OPT-OUTER-5',
            'OPT-OUTER-6',
            'KET-TSR-6',
            'KET-TSR-7',
            'BRA-TSR-6',
            'BRA-TSR-7',
            'OPT-TSR-7',
            'OPT-TSR-8',
        ]
    )


    # build the trs
    return trs


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