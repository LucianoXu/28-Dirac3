
'''
all the rewriting rules for Dirac notation
'''

from __future__ import annotations
from .theory.trs import *
from .theory.dirac_syntax import *

from .components.py_cscalar import PyCScalar
from .components.wolfram_cscalar import WolframCScalar

rules = []

# CScalar = PyCScalar
CScalar = WolframCScalar

C0 = ScalarC(CScalar.zero())
C1 = ScalarC(CScalar.one())
C2 = ScalarC(CScalar.add(CScalar.one(), CScalar.one()))


# parser
from .parser import parse
    


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
    lhs = parse("PAIR(FST(p), SND(p))"),
    rhs = parse("p")
)
rules.append(BASIS_3)

#################################################
# Delta
def delta_1_rewrite(rule, term):
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
    lhs = "delta(u, PAIR(s, t))",
    rhs = "delta(fst(u), s) MLTS delta(snd(u), t)",
    rewrite_method=delta_1_rewrite
)
rules.append(DELTA_1)


def delta_2_rewrite(rule, term):
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
    lhs = "delta(fst(u), fst(v)) MLTS delta(snd(u), snd(v))",
    rhs = "delta(u, v)",
    rewrite_method=delta_2_rewrite
)
rules.append(DELTA_2)


#################################################
# Scalar

def scr_complex_1_rewrite(rule, term):
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


def scr_complex_2_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            if isinstance(term.args[i], ScalarC):
                for j in range(i+1, len(term.args)):
                    if isinstance(term.args[j], ScalarC):

                        new_args = (ScalarC(CScalar.add(term.args[i].args[0], term.args[j].args[0])),) + term.remained_terms(i, j)

                        return ScalarAdd(*new_args)

SCR_COMPLEX_2 = TRSRule(
    lhs="C(a) ADDS C(b)", 
    rhs="C(a + b)",
    rewrite_method=scr_complex_2_rewrite
)
rules.append(SCR_COMPLEX_2)

def scr_complex_3_rewrite(rule, term):
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

def scr_complex_4_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            if isinstance(term.args[i], ScalarMlt):
                for j in range(len(term.args[i].args)):
                    if isinstance(term[i][j], ScalarC):
                        S0 = ScalarMlt(*term[i].args[:j], *term[i].args[j+1:])
                        for k in range(len(term.args)):
                            if S0 == term.args[k]:
                                new_args = (ScalarMlt(ScalarC(CScalar.add(term[i][j].args[0], CScalar.one())), term[k]),)
                                new_args += term.remained_terms(i, k)
                                return ScalarAdd(*new_args)
                            
SCR_COMPLEX_4 = TRSRule(
    lhs = "(C(a) MLTS S0) ADDS S0",
    rhs = "C(a + 1) MLTS S0",
    rewrite_method=scr_complex_4_rewrite
)
rules.append(SCR_COMPLEX_4)

def scr_complex_5_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            if isinstance(term.args[i], ScalarMlt):
                for j in range(len(term.args[i].args)):
                    if isinstance(term[i][j], ScalarC):
                        S0 = ScalarMlt(*term[i].args[:j], *term[i].args[j+1:])
                        for k in range(i+1, len(term.args)):
                            if isinstance(term.args[k], ScalarMlt):
                                for l in range(len(term.args[k].args)):
                                    if isinstance(term[k][l], ScalarC):
                                        S1 = ScalarMlt(*term[k].args[:l], *term[k].args[l+1:])
                                        if S0 == S1:
                                            new_args = (ScalarMlt(ScalarC(CScalar.add(term[i][j].args[0], term[k][l].args[0])), S0),)
                                            new_args += term.remained_terms(i, k)
                                            return ScalarAdd(*new_args)

SCR_COMPLEX_5 = TRSRule(
    lhs = "(C(a) MLTS S0) ADDS (C(b) MLTS S0)",
    rhs = "C(a + b) MLTS S0",
    rewrite_method=scr_complex_5_rewrite
)
rules.append(SCR_COMPLEX_5)

def scr_complex_6_rewrite(rule, term):
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

def scr_complex_7_rewrite(rule, term):
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


def scr_complex_8_rewrite(rule, term):
    if isinstance(term, ScalarMlt):
        for i in range(len(term.args)):
            if isinstance(term.args[i], ScalarC):
                for j in range(i+1, len(term.args)):
                    if isinstance(term.args[j], ScalarC):

                        new_args = (ScalarC(CScalar.mlt(term.args[i].args[0], term.args[j].args[0])),) + term.remained_terms(i, j)

                        return ScalarMlt(*new_args)

SCR_COMPLEX_8 = TRSRule(
    lhs="C(a) MLTS C(b)",
    rhs="C(a * b)",
    rewrite_method=scr_complex_8_rewrite
)
rules.append(SCR_COMPLEX_8)

def scr_complex_9_rewrite(rule, term):
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


def scr_complex_10_rewrite(rule, term):
    if isinstance(term, ScalarConj):
        if isinstance(term.args[0], ScalarC):
            return ScalarC(CScalar.conj(term.args[0].args[0]))
SCR_COMPLEX_10 = TRSRule(
    lhs="CONJS(C(a))",
    rhs="C(a ^*)",
    rewrite_method=scr_complex_10_rewrite
)
rules.append(SCR_COMPLEX_10)
    

def scr_complex_11_rewrite(rule, term):
    if isinstance(term, ScalarConj):
        if isinstance(term.args[0], ScalarDelta):
            return term.args[0]
        
SCR_COMPLEX_11 = TRSRule(
    lhs="CONJS(delta(a, b))",
    rhs="delta(a, b)",
    rewrite_method=scr_complex_11_rewrite
)
rules.append(SCR_COMPLEX_11)


def scr_complex_12_rewrite(rule, term):
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


def scr_complex_13_rewrite(rule, term):
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
    lhs = parse(r''' CONJS(B DOT K) '''),
    rhs = parse(r''' ADJB(K) DOT ADJK(B) ''')
)
rules.append(SCR_COMPLEX_15)

def scr_dot_1(rule, term):
    if isinstance(term, ScalarDot):
        if isinstance(term.args[0], BraZero):
            return C0
SCR_DOT_1 = TRSRule(
    lhs = "0B DOT K0",
    rhs = "C(0)",
    rewrite_method=scr_dot_1
)
rules.append(SCR_DOT_1)

def scr_dot_2(rule, term):
    if isinstance(term, ScalarDot):
        if isinstance(term.args[1], KetZero):
            return C0
SCR_DOT_2 = TRSRule(
    lhs = "B0 DOT 0K",
    rhs = "C(0)",
    rewrite_method=scr_dot_2
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

def scr_dot_5(rule, term):
    if isinstance(term, ScalarDot):
        if isinstance(term.args[0], BraAdd):
            new_args = tuple(ScalarDot(arg, term.args[1]) for arg in term.args[0].args)
            return ScalarAdd(*new_args)
SCR_DOT_5 = TRSRule(
    lhs = "(B1 ADDS B2) DOT K0",
    rhs = "(B1 DOT K0) ADDS (B2 DOT K0)",
    rewrite_method=scr_dot_5
)
rules.append(SCR_DOT_5)

def scr_dot_6(rule, term):
    if isinstance(term, ScalarDot):
        if isinstance(term.args[1], KetAdd):
            new_args = tuple(ScalarDot(term.args[0], arg) for arg in term.args[1].args)
            return ScalarAdd(*new_args)
SCR_DOT_6 = TRSRule(
    lhs = "B0 DOT (K1 ADDS K2)",
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
    lhs = parse(r''' (B MLTB O) DOT K '''),
    rhs = parse(r''' B DOT (O MLTK K) ''')
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
    lhs = parse(r'''ADJK(ZEROB)'''),
    rhs = parse(r'''ZEROK''')
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
    rhs = parse(r'''CONJS(S0) SCRK ADJK(K0)'''),
)
rules.append(KET_ADJ_4)

def ket_adj_5_rewrite(rule, term):
    if isinstance(term, KetAdj):
        if isinstance(term.args[0], BraAdd):
            new_args = tuple(KetAdj(arg) for arg in term.args[0].args)
            return KetAdd(*new_args)
KET_ADJ_5 = TRSRule(
    lhs = "ADJK(B1 ADDB B2)",
    rhs = "ADJK(B1) ADDB ADJK(B2)",
    rewrite_method=ket_adj_5_rewrite
)
rules.append(KET_ADJ_5)

KET_ADJ_6 = TRSRule(
    lhs = parse(r'''ADJK(B MLTB O)'''),
    rhs = parse(r'''ADJO(O) MLTK ADJK(B)''')
)
rules.append(KET_ADJ_6)

KET_ADJ_7 = TRSRule(
    lhs = parse(r''' ADJK(B1 TSRB B2) '''),
    rhs = parse(r''' ADJK(B1) TSRK ADJK(B2) ''')
)
rules.append(KET_ADJ_7)


def ket_scal_1(rule, term):
    if isinstance(term, KetScal):
        if term.args[0] == C0:
            return KetZero()
        
KET_SCAL_1 = TRSRule(
    lhs = "C(0) SCRK K0",
    rhs = "0K",
    rewrite_method=ket_scal_1
)
rules.append(KET_SCAL_1)

def ket_scal_2(rule, term):
    if isinstance(term, KetScal):
        if term.args[0] == C1:
            return term.args[1]
KET_SCAL_2 = TRSRule(
    lhs = "C(1) SCRK K0",
    rhs = "K0",
    rewrite_method=ket_scal_2
)
rules.append(KET_SCAL_2)

KET_SCAL_3 = TRSRule(
    lhs = parse(r'''S0 SCRK ZEROK'''),
    rhs = parse(r''' ZEROK ''')
)
rules.append(KET_SCAL_3)

    
KET_SCAL_4 = TRSRule(
    lhs = parse(r'''S1 SCRK (S2 SCRK K0)'''),
    rhs = parse(r'''(S1 MLTS S2) SCRK K0'''),
)
rules.append(KET_SCAL_4)


def ket_scal_5_rewrite(rule, term):
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


def ket_add_1(rule, term):
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

def ket_add_2(rule, term):
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

def ket_add_3(rule, term):
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
    rhs = "C(1 + S0) SCRK K0",
    rewrite_method=ket_add_3
)
rules.append(KET_ADD_3)

def ket_add_4(rule, term):
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
    lhs = parse(r'''ZEROO MLTK K0'''),
    rhs = parse(r'''ZEROK''')
)
rules.append(KET_MUL_1)

KET_MUL_2 = TRSRule(
    lhs = parse(r'''O0 MLTK ZEROK'''),
    rhs = parse(r'''ZEROK''')
)
rules.append(KET_MUL_2)

KET_MUL_3 = TRSRule(
    lhs = parse(r'''ONEO MLTK K0'''),
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


def ket_mul_6_rewrite(rule, term):
    if isinstance(term, KetApply) and isinstance(term[0], OpAdd):
        new_args = tuple(KetApply(arg, term[1]) for arg in term[0].args)
        return KetAdd(*new_args)
KET_MUL_6 = TRSRule(
    lhs = "(O1 ADDO O2) MLTK K0",
    rhs = "(O1 MLTK K0) ADDK (O2 MLTK K0)",
    rewrite_method=ket_mul_6_rewrite
)
rules.append(KET_MUL_6)


def ket_mul_7_rewrite(rule, term):
    if isinstance(term, KetApply) and isinstance(term[1], KetAdd):
        new_args = tuple(KetApply(term[0], arg) for arg in term[1].args)
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
    rhs = parse(r'''(O1 MLTK KET(FST(t))) TSRK (O2 MLTK KET(SND(T)))''')
)
rules.append(KET_MUL_11)

KET_MUL_12 = TRSRule(
    lhs = parse(r'''(O1 TSRO O2) MLTK (K1 TSRK K2)'''),
    rhs = parse(r'''(O1 MLTK K1) TSRK (O2 MLTK K2)''')
)
rules.append(KET_MUL_12)

KET_TSR_1 = TRSRule(
    lhs = parse(r'''ZEROK TSRK K0'''),
    rhs = parse(r'''ZEROK''')
)
rules.append(KET_TSR_1)

KET_TSR_2 = TRSRule(
    lhs = parse(r'''K0 TSRK ZEROK'''),
    rhs = parse(r'''ZEROK''')
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

def ket_tsr_6_rewrite(rule, term):
    if isinstance(term, KetTensor) and isinstance(term[0], KetAdd):
        new_args = tuple(KetTensor(arg, term[1]) for arg in term[0].args)
        return KetAdd(*new_args)
KET_TSR_6 = TRSRule(
    lhs = "(K1 ADDK K2) TSRK K0",
    rhs = "(K1 TSRK K0) ADDK (K2 TSRK K0)",
    rewrite_method=ket_tsr_6_rewrite
)
rules.append(KET_TSR_6)

def ket_tsr_7_rewrite(rule, term):
    if isinstance(term, KetTensor) and isinstance(term[1], KetAdd):
        new_args = tuple(KetTensor(term[0], arg) for arg in term[1].args)
        return KetAdd(*new_args)
KET_TSR_7 = TRSRule(
    lhs = "K0 TSRK (K1 ADDK K2)",
    rhs = "(K0 TSRK K1) ADDK (K0 TSRK K2)",
    rewrite_method=ket_tsr_7_rewrite
)
rules.append(KET_TSR_7)

# build the trs
diractrs = TRS(rules)