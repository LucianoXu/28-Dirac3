
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
    '''
    This trs only deals with label related rewritings.
    '''
    
    def parse(s: str) -> TRSTerm:
        return parser.parse(s)


    # prepare the rules
    rules = []

    REG_1 = TRSRule(
        "REG-1",
        lhs = parse("FSTR(PAIRR(s, t))"),
        rhs = parse("s")
    )
    rules.append(REG_1)

    REG_2 = TRSRule(
        "REG-2",
        lhs = parse("SNDR(PAIRR(s, t))"),
        rhs = parse("t")
    )
    rules.append(REG_2)

    REG_3 = TRSRule(
        "REG-3",
        lhs = parse("PAIRR(FSTR(s), SNDR(s))"),
        rhs = parse("s")
    )
    rules.append(REG_3)


    ########################################
    # register sets

    def rset_1_rewrite(rule, trs, term, side_info):
        if isinstance(term, UnionRSet):
            for i, s in enumerate(term.args):
                if s == EmptyRSet():
                    return UnionRSet(*term.remained_terms(i))
    RSET_1 = TRSRule(
        "RSET-1",
        lhs = "S UNIONR ESETR",
        rhs = "S",
        rewrite_method=rset_1_rewrite
    )
    rules.append(RSET_1)

    def rset_2_rewrite(rule, trs, term, side_info):
        if isinstance(term, UnionRSet):
            for i in range(len(term.args)):
                for j in range(i+1, len(term.args)):
                    if term.args[i] == term.args[j]:
                        return UnionRSet(*term.remained_terms(j))
    RSET_2 = TRSRule(
        "RSET-2",
        lhs = "S UNIONR S",
        rhs = "S",
        rewrite_method=rset_2_rewrite
    )
    rules.append(RSET_2)

    def rset_3_rewrite(rule, trs, term, side_info):
        if isinstance(term, UnionRSet):
            for i in range(len(term.args)):
                si = term.args[i]
                if isinstance(si, RegRSet):
                    for j in range(i, len(term.args)):
                        sj = term.args[j]
                        if isinstance(sj, RegRSet):
                            if ((isinstance(si.args[0], QRegFst) and isinstance(sj.args[0], QRegSnd)) or \
                                (isinstance(si.args[0], QRegSnd) and isinstance(sj.args[0], QRegFst))) and si.args[0].args[0] == sj.args[0].args[0]:
                                return UnionRSet(*term.remained_terms(i, j), si.args[0].args[0])
    RSET_3 = TRSRule(
        "RSET-3",
        lhs = "SETR(FST(R)) UNIONR SETR(SND(R))",
        rhs = "R",
        rewrite_method=rset_3_rewrite
    )
    rules.append(RSET_3)
    

    RSET_4 = TRSRule(
        "RSET-4",
        lhs = parse(" S0 SUBR ESETR "),
        rhs = parse(" S0 ")
    )
    rules.append(RSET_4)


    RSET_5 = TRSRule(
        "RSET-5",
        lhs = parse(" ESETR SUBR S0 "),
        rhs = parse(" ESETR ")
    )
    rules.append(RSET_5)

    RSET_6 = TRSRule(
        "RSET-6",
        lhs = parse(" S0 SUBR S0 "),
        rhs = parse(" ESETR ")
    )
    rules.append(RSET_6)

    def rset_7_rewrite(rule, trs, term, side_info):
        if isinstance(term, SubRSet) and isinstance(term.args[0], UnionRSet):
            return UnionRSet(*tuple(SubRSet(item, term.args[1]) for item in term.args[0]))

    RSET_7 = TRSRule(
        "RSET-7",
        lhs = " (S1 UNIONR S2) SUBR X ",
        rhs = " (S1 SUBR X) UNIONR (S2 SUBR X) ",
        rewrite_method=rset_7_rewrite
    )
    rules.append(RSET_7)


    def rset_8_rewrite(rule, trs, term, side_info):
        if isinstance(term, SubRSet) and isinstance(term.args[1], UnionRSet):
            return SubRSet(SubRSet(term.args[0], term.args[1].args[0]), UnionRSet(*term.args[1].remained_terms(0)))

    RSET_8 = TRSRule(
        "RSET-8",
        lhs = " S1 SUBR (S2 UNIONR S3) ",
        rhs = " (S1 SUBR S2) SUBR S3 ",
        rewrite_method=rset_8_rewrite
    )
    rules.append(RSET_8)

    def rset_9_rewrite(rule, trs, term, side_info):
        if isinstance(term, UnionRSet):
            for i, si in enumerate(term.args):
                if isinstance(si, RegRSet):
                    for j, sj in enumerate(term.args):
                        if i == j:
                            continue
                        if isinstance(sj, RegRSet):
                            if QReg.is_in(si.args[0], sj.args[0]):
                                return UnionRSet(*term.remained_terms(i))
    RSET_9 = TRSRule(
        "RSET-9",
        lhs = " SETR(R1) UNIONR SETR(R2) (R1 is in R2) ",
        rhs = "SETR(R2)",
        rewrite_method=rset_9_rewrite
    )
    rules.append(RSET_9)

    def rset_10_rewrite(rule, trs, term, side_info):
        if isinstance(term, SubRSet) and isinstance(term.args[0], RegRSet) and isinstance(term.args[1], RegRSet):
            if QReg.is_in(term.args[0].args[0], term.args[1].args[0]):
                return EmptyRSet()
    RSET_10 = TRSRule(
        "RSET-10",
        lhs = " SETR(R1) SUBR SETR(R2) (R1 is in R2) ",
        rhs = "ESETR",
        rewrite_method=rset_10_rewrite
    )
    rules.append(RSET_10)


    def rset_11_rewrite(rule, trs, term, side_info):
        if isinstance(term, SubRSet) and isinstance(term.args[0], RegRSet) and isinstance(term.args[1], RegRSet):
            if QReg.is_in(term.args[1].args[0], term.args[0].args[0]):
                return UnionRSet(
                    SubRSet(RegRSet(QRegFst(term.args[0].args[0])), term.args[1]),
                    SubRSet(RegRSet(QRegSnd(term.args[0].args[0])), term.args[1]),
                    )
    RSET_11 = TRSRule(
        "RSET-11",
        lhs = " SETR(R2) SUBR SETR(R1) (R1 is in R2) ",
        rhs = " SETR(FSTR(R2) SUBR SETR(R1)) UNIONR SETR(SNDR(R2) SUBR SETR(R1)) ",
        rewrite_method=rset_11_rewrite
    )
    rules.append(RSET_11)

    def rset_12_rewrite(rule, trs, term, side_info):
        if isinstance(term, SubRSet) and isinstance(term.args[0], RegRSet) and isinstance(term.args[1], RegRSet):
            if QReg.is_disj(term.args[0].args[0], term.args[1].args[0]):
                return term.args[0]
    RSET_12 = TRSRule(
        "RSET-12",
        lhs = " SETR(R1) SUBR SETR(R2) (R1 || R2) ",
        rhs = " SETR(R1) ",
        rewrite_method=rset_12_rewrite
    )
    rules.append(RSET_12)


    ######################################################
    # labelled dirac notation rules
    
    TSR_DECOMP_1 = TRSRule(
        "TSR-DECOMP-1",
        lhs = parse(''' KET(PAIR(s, t))[PAIRR(Q, R)] '''),
        rhs = parse(''' KET(s)[Q] TSRKL KET(t)[R] ''')
    )
    rules.append(TSR_DECOMP_1)


    TSR_DECOMP_2 = TRSRule(
        "TSR-DECOMP-2",
        lhs = parse(''' BRA(PAIR(s, t))[PAIRR(Q, R)] '''),
        rhs = parse(''' BRA(s)[Q] TSRBL BRA(t)[R] ''')
    )
    rules.append(TSR_DECOMP_2)

    TSR_DECOMP_3A = TRSRule(
        "TSR-DECOMP-3A",
        lhs = parse(''' 0X[PAIRR(Q1, Q2); R] '''),
        rhs = parse(''' (0X[Q1; FSTR(R)]) TSROL (0X[Q2; SNDR(R)]) ''')
    )
    rules.append(TSR_DECOMP_3A)

    TSR_DECOMP_3B = TRSRule(
        "TSR-DECOMP-3B",
        lhs = parse(''' 0X[Q; PAIRR(R1, R2)] '''),
        rhs = parse(''' (0X[FSTR(Q); R1]) TSROL (0X[SNDR(Q2); R2]) ''')
    )
    rules.append(TSR_DECOMP_3B)

    TSR_DECOMP_3C = TRSRule(
        "TSR-DECOMP-3C",
        lhs = parse(''' 1O[PAIRR(Q, R)] '''),
        rhs = parse(''' (1O[Q]) TSROL (1O[R]) ''')
    )
    rules.append(TSR_DECOMP_3C)

    TSR_DECOMP_3D = TRSRule(
        "TSR-DECOMP-3D",
        lhs = parse(''' 1O[PAIRR(Q1, Q2); R] '''),
        rhs = parse(''' (1O[Q1; FSTR(R)]) TSROL (1O[Q2; SNDR(R)]) ''')
    )
    rules.append(TSR_DECOMP_3D)

    TSR_DECOMP_3E = TRSRule(
        "TSR-DECOMP-3E",
        lhs = parse(''' 1O[Q; PAIRR(R1, R2)] '''),
        rhs = parse(''' (1O[FSTR(Q); R1]) TSROL (1O[SNDR(Q2); R2]) ''')
    )
    rules.append(TSR_DECOMP_3E)

    def tsr_decomp_3_rewrite(rule, trs, term, side_info):
        if isinstance(term, Labelled1) and isinstance(term.args[0], (KetTensor, BraTensor, OpTensor)) and isinstance(term.args[1], QRegPair):
            if isinstance(term.args[0], KetTensor):
                T = KetTensorL
            elif isinstance(term.args[0], BraTensor):
                T = BraTensorL
            elif isinstance(term.args[0], OpTensor):
                T = OpTensorL
            else:
                raise Exception()
            
            return T(
                Labelled1(term.args[0].args[0], term.args[1].args[0]),
                Labelled1(term.args[0].args[1], term.args[1].args[1])
            )
    TSR_DECOMP_3 = TRSRule(
        "TSR-DECOMP-3",
        lhs = " (A {TSRK/TSRB/TSRO} B)[PAIRR(Q, R)] ",
        rhs = " (A[Q]) {TSRKL/TSRBL/TSROL} (B[R]) ",
        rewrite_method = tsr_decomp_3_rewrite
    )
    rules.append(TSR_DECOMP_3)

    TSR_DECOMP_4 = TRSRule(
        "TSR-DECOMP-4",
        lhs = parse(''' (A TSRO B)[PAIRR(Q1, Q2); R] '''),
        rhs = parse(''' (A[Q1; FSTR(R)]) TSROL (B[Q2; SNDR(R)]) ''')
    )
    rules.append(TSR_DECOMP_4)

    TSR_DECOMP_5 = TRSRule(
        "TSR-DECOMP-5",
        lhs = parse(''' (A TSRO B)[Q; PAIRR(R1, R2)] '''),
        rhs = parse(''' (A[FSTR(Q); R1]) TSROL (B[SNDR(Q); R2]) ''')
    )
    rules.append(TSR_DECOMP_5)

    def tsr_comp_1_rewrite(rule, trs, term, side_info):
        if isinstance(term, OpTensorL):
            for i, oi in enumerate(term.args):
                if isinstance(oi, Labelled2) and isinstance(oi.args[1], QRegFst) and isinstance(oi.args[2], QRegFst):
                    for j, oj in enumerate(term.args):
                        if isinstance(oj, Labelled2) and isinstance(oj.args[1], QRegSnd) and isinstance(oj.args[2], QRegSnd):
                            if oi.args[1].args[0] == oj.args[1].args[0] and oi.args[2].args[0] == oj.args[2].args[0]:
                                return OpTensorL(
                                    Labelled2(
                                        OpTensor(oi.args[0], oj.args[0]), 
                                        oi.args[1].args[0], oi.args[2].args[0]
                                        ),
                                    *term.remained_terms(i, j))
    TSR_COMP_1 = TRSRule(
        "TSR-COMP-1",
        lhs = " (A[FSTR(Q); FSTR(R)]) TSROL (B[SNDR(Q); SNDR(R)]) ",
        rhs = " (A TSRO B)[Q; R] ",
        rewrite_method = tsr_comp_1_rewrite
    )
    rules.append(TSR_COMP_1)

    def tsr_comp_2_rewrite(rule, trs, term, side_info):
        if isinstance(term, (KetTensorL, BraTensorL, OpTensorL)):
            for i, oi in enumerate(term.args):
                if isinstance(oi, Labelled1) and isinstance(oi.args[1], QRegFst):
                    for j, oj in enumerate(term.args):
                        if isinstance(oj, Labelled1) and isinstance(oj.args[1], QRegSnd):
                            if oi.args[1].args[0] == oj.args[1].args[0]:
                                if isinstance(term, KetTensorL):
                                    T = KetTensor
                                elif isinstance(term, BraTensorL):
                                    T = BraTensor
                                else:
                                    T = OpTensor

                                return type(term)(
                                    Labelled1(
                                        T(oi.args[0], oj.args[0]), 
                                        oi.args[1].args[0]),
                                    *term.remained_terms(i, j))
    TSR_COMP_2 = TRSRule(
        "TSR-COMP-2",
        lhs = " (A[FSTR(Q)]) {TSRKL/TSRBL/TSROL} (B[SNDR(Q)]) ",
        rhs = " (A {TSRK/TSRB/TSRO} B)[Q] ",
        rewrite_method = tsr_comp_2_rewrite
    )
    rules.append(TSR_COMP_2)

    def dot_tsr_1_rewrite(rule, trs, term, side_info):
        if isinstance(term, OpApplyL) and isinstance(term.args[0], Labelled2) and isinstance(term.args[1], Labelled2):
            if QReg.is_disj(term.args[0].args[2], term.args[1].args[1]):
                return OpTensorL(term.args[0], term.args[1])
    DOT_TSR_1 = TRSRule(
        "DOT-TSR-1",
        lhs = " (A[Q;R]) MLTOL (B[S;T]) (R || S) ",
        rhs = " (A[Q;R]) TSROL (B[S;T]) ",
        rewrite_method = dot_tsr_1_rewrite
    )
    rules.append(DOT_TSR_1)


    LABEL_LIFT_1 = TRSRule(
        "LABEL-LIFT-1",
        lhs = parse(''' ADJL(A[R]) '''),
        rhs = parse(''' (ADJ(A))[R]''')
    )
    rules.append(LABEL_LIFT_1)

    LABEL_LIFT_2 = TRSRule(
        "LABEL-LIFT-2",
        lhs = parse(''' ADJL(A[Q; R]) '''),
        rhs = parse(''' (ADJ(A))[Q; R]''')
    )
    rules.append(LABEL_LIFT_2)


    LABEL_LIFT_3 = TRSRule(
        "LABEL-LIFT-3",
        lhs = parse(''' (S SCR A)[R] '''),
        rhs = parse(''' S SCR (A[R])''')
    )
    rules.append(LABEL_LIFT_3)

    LABEL_LIFT_4 = TRSRule(
        "LABEL-LIFT-4",
        lhs = parse(''' (S SCR A)[Q; R] '''),
        rhs = parse(''' S SCR (A[Q; R])''')
    )
    rules.append(LABEL_LIFT_4)

    def label_lift_5_rewrite(rule, trs, term, side_info):
        if isinstance(term, Labelled1) and isinstance(term.args[0], Add):
            return AddL(*tuple(Labelled1(t, term.args[1]) for t in term.args[0].args))
    LABEL_LIFT_5 = TRSRule(
        "LABEL-LIFT-5",
        lhs = " (A ADD B)[R] ",
        rhs = " (A[R]) ADDL (B[R]) ",
        rewrite_method = label_lift_5_rewrite
    )
    rules.append(LABEL_LIFT_5)

    def label_lift_6_rewrite(rule, trs, term, side_info):
        if isinstance(term, Labelled2) and isinstance(term.args[0], Add):
            return AddL(*tuple(Labelled2(t, term.args[1], term.args[2]) for t in term.args[0].args))
    LABEL_LIFT_6 = TRSRule(
        "LABEL-LIFT-6",
        lhs = " (A ADD B)[Q; R] ",
        rhs = " (A[Q; R]) ADDL (B[Q; R]) ",
        rewrite_method = label_lift_6_rewrite
    )
    rules.append(LABEL_LIFT_6)

    def label_lift_7_rewrite(rule, trs, term, side_info):
        if isinstance(term, AddL):
            for i in range(len(term.args)):
                ti = term.args[i]
                for j in range(i + 1, len(term.args)):
                    tj = term.args[j]
                    if ti == tj:
                        return AddL(
                            ScalL(
                                CScalar.add(CScalar.one(), CScalar.one()),
                                ti),
                            *term.remained_terms(i, j)
                        )
    LAEBL_LIFT_7 = TRSRule(
        "LABEL-LIFT-7",
        lhs = " A ADDL A ",
        rhs = " C(1+1) SCRL A ",
        rewrite_method = label_lift_7_rewrite
    )
    rules.append(LAEBL_LIFT_7)


    def label_lift_8_rewrite(rule, trs, term, side_info):
        if isinstance(term, AddL):
            for i in range(len(term.args)):
                ti = term.args[i]
                if isinstance(ti, ScalL):
                    for j in range(i + 1, len(term.args)):
                        tj = term.args[j]
                        if ti.args[1] == tj:
                            return AddL(
                                ScalL(
                                    ScalarAdd(CScalar.one(), ti.args[0]),
                                    tj),
                                *term.remained_terms(i, j)
                            )
    LAEBL_LIFT_8 = TRSRule(
        "LABEL-LIFT-8",
        lhs = " (S SCRL A) ADDL A ",
        rhs = " (S ADDS C(1)) SCRL A ",
        rewrite_method = label_lift_8_rewrite
    )
    rules.append(LAEBL_LIFT_8)

    def label_lift_9_rewrite(rule, trs, term, side_info):
        if isinstance(term, AddL):
            for i in range(len(term.args)):
                ti = term.args[i]
                if isinstance(ti, ScalL):
                    for j in range(i + 1, len(term.args)):
                        tj = term.args[j]
                        if isinstance(tj, ScalL) and ti.args[1] == tj.args[1]:
                            return AddL(
                                ScalL(
                                    ScalarAdd(ti.args[0], tj.args[0]),
                                    ti.args[1]),
                                *term.remained_terms(i, j)
                            )
    LAEBL_LIFT_9 = TRSRule(
        "LABEL-LIFT-9",
        lhs = " (S1 SCRL A) ADDL (S2 SCRL A) ",
        rhs = " (S1 ADDS S2) SCRL A ",
        rewrite_method = label_lift_9_rewrite
    )
    rules.append(LAEBL_LIFT_9)

    LABEL_LIFT_10 = TRSRule(
        "LABEL-LIFT-10",
        lhs = parse(''' (A[Q; R]) MLTOL (B[R; S]) '''),
        rhs = parse(''' (A MLTO B)[Q; S] ''')
    )
    rules.append(LABEL_LIFT_10)

    LABEL_LIFT_11 = TRSRule(
        "LABEL-LIFT-11",
        lhs = parse(''' (A[Q; R]) MLTOL (B[R]) '''),
        rhs = parse(''' (A MLTO B)[Q; R] ''')
    )
    rules.append(LABEL_LIFT_11)

    LABEL_LIFT_12 = TRSRule(
        "LABEL-LIFT-12",
        lhs = parse(''' (A[Q]) MLTOL (B[Q; R]) '''),
        rhs = parse(''' (A MLTO B)[Q; R] ''')
    )
    rules.append(LABEL_LIFT_12)

    LABEL_LIFT_13 = TRSRule(
        "LABEL-LIFT-13",
        lhs = parse(''' (A[Q; R]) MLTKL (B[R]) '''),
        rhs = parse(''' (A MLTK B)[Q] ''')
    )
    rules.append(LABEL_LIFT_13)

    LABEL_LIFT_14 = TRSRule(
        "LABEL-LIFT-14",
        lhs = parse(''' (A[Q]) MLTBL (B[Q; R]) '''),
        rhs = parse(''' (A MLTB B)[R] ''')
    )
    rules.append(LABEL_LIFT_14)

    def label_lift_15_rewrite(rule, trs, term, side_info):
        if isinstance(term, (KetApplyL, BraApplyL, OpApplyL)) and isinstance(term.args[0], Labelled1) and isinstance(term.args[1], Labelled1) and term.args[0].args[1] == term.args[1].args[1]:
            if isinstance(term, KetApplyL):
                T = KetApply
            elif isinstance(term, BraApplyL):
                T = BraApply
            elif isinstance(term, OpApplyL):
                T = OpApply
            else:
                raise Exception()
            return Labelled1(T(term.args[0].args[0], term.args[1].args[0]), term.args[0].args[1])


    LABEL_LIFT_15 = TRSRule(
        "LABEL-LIFT-15",
        lhs = " (A[R]) {MLTOL/MLTKL/MLTBL} (B[R]) ",
        rhs = " (A {MLTOL/MLTKL/MLTBL} B)[R] ",
        rewrite_method = label_lift_15_rewrite
    )
    rules.append(LABEL_LIFT_15)


    LABEL_LIFT_16 = TRSRule(
        "LABEL-LIFT-16",
        lhs = parse(''' (A[R]) DOTL (B[R]) '''),
        rhs = parse(''' A DOT B ''')
    )
    rules.append(LABEL_LIFT_16)


    LABEL_LIFT_17 = TRSRule(
        "LABEL-LIFT-17",
        lhs = parse(''' (K0 OUTER B0)[R] '''),
        rhs = parse(''' (K0[R]) OUTERL (B0[R]) ''')
    )
    rules.append(LABEL_LIFT_17)

    LABEL_LIFT_18 = TRSRule(
        "LABEL-LIFT-18",
        lhs = parse(''' (K0 OUTER B0)[Q; R] '''),
        rhs = parse(''' (K0[Q]) OUTERL (B0[R]) ''')
    )
    rules.append(LABEL_LIFT_18)

    OPT_EXT_1 = TRSRule(
        "OPT-EXT-1",
        lhs = parse(''' A[R; R] '''),
        rhs = parse(''' A[R] ''')
    )
    rules.append(OPT_EXT_1)

    def opt_ext_2_rewrite(rule, trs, term, side_info):
        if isinstance(term, OpApplyL) and isinstance(term.args[0], Labelled1) and isinstance(term.args[1], Labelled1):

            p = QReg.subreg_pos(term.args[0].args[1], term.args[1].args[1])
            if p is not None:
                extA = term.args[0].args[0]
                while p != "":
                    if p[-1] == "0":
                        extA = OpTensor(extA, OpOne())
                    elif p[-1] == "1":
                        extA = OpTensor(OpOne(), extA)
                    else:
                        raise Exception()
                    p = p[:-1]

                return Labelled1(
                    OpApply(extA, term.args[1].args[0]),
                    term.args[1].args[1]
                )
    OPT_EXT_2 = TRSRule(
        "OPT-EXT-2",
        lhs = "(A[Q]) MLTOL (B[R]) (Q is a subterm of R at p)",
        rhs = "(ext(A, p) MLTO B)[R]",
        rewrite_method = opt_ext_2_rewrite
    )
    rules.append(OPT_EXT_2)


    def opt_ext_3_rewrite(rule, trs, term, side_info):
        if isinstance(term, OpApplyL) and isinstance(term.args[0], Labelled1) and isinstance(term.args[1], Labelled1):

            p = QReg.subreg_pos(term.args[1].args[1], term.args[0].args[1])
            if p is not None:
                extB = term.args[1].args[0]
                while p != "":
                    if p[-1] == "0":
                        extB = OpTensor(extB, OpOne())
                    elif p[-1] == "1":
                        extB = OpTensor(OpOne(), extB)
                    else:
                        raise Exception()
                    p = p[:-1]

                return Labelled1(
                    OpApply(term.args[0].args[0], extB),
                    term.args[0].args[1]
                )
    OPT_EXT_3 = TRSRule(
        "OPT-EXT-3",
        lhs = "(A[Q]) MLTOL (B[R]) (R is a subterm of Q at p)",
        rhs = "(A MLTO ext(B, p))[Q]",
        rewrite_method = opt_ext_3_rewrite
    )
    rules.append(OPT_EXT_3)



    def label_sum_1_rewrite(rule, trs, term, side_info):
        if isinstance(term, Labelled1) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_vars, Labelled1(term.args[0].body, term.args[1]))
    LABEL_SUM_1 = TRSRule(
        "LABEL-SUM-1",
        lhs = " SUM(x, T, A)[R] ",
        rhs = " SUM(x, T, A[R]) ",
        rewrite_method = label_sum_1_rewrite
    )
    rules.append(LABEL_SUM_1)


    def label_sum_2_rewrite(rule, trs, term, side_info):
        if isinstance(term, Labelled2) and isinstance(term.args[0], Sum):
            return Sum(term.args[0].bind_vars, Labelled2(term.args[0].body, term.args[1], term.args[2]))
    LABEL_SUM_2 = TRSRule(
        "LABEL-SUM-2",
        lhs = " SUM(x, T, A)[Q; R] ",
        rhs = " SUM(x, T, A[Q; R]) ",
        rewrite_method = label_sum_2_rewrite
    )
    rules.append(LABEL_SUM_2)


    def label_sum_3_rewrite(rule, trs, term, side_info):
        if isinstance(term, ScalarDotL) and isinstance(term.args[0], SumS) or isinstance(term, (KetApplyL, BraApplyL, OpApplyL)) and isinstance(term.args[0], Sum):

            # we have to rename if necessary
            if set(v[0].name for v in term.args[0].bind_vars) & term.args[1].free_variables() == set():
                new_var = var_rename_ls(term.args[0].variables() | term.args[1].variables(), len(term.args[0].bind_vars))
                renamed_sum = term.args[0].rename_bind(tuple(TRSVar(v) for v in new_var))
            else:
                renamed_sum = term.args[0]

            combined_term = type(term)(renamed_sum.body, term.args[1])
            norm_term = trs.normalize(combined_term, **side_info['trs-args'])
            if norm_term != combined_term:
                if type(term) == ScalarDotL:
                    return SumS(renamed_sum.bind_vars, norm_term)
                else:
                    return Sum(renamed_sum.bind_vars, norm_term)
    LABEL_SUM_3 = TRSRule(
        "LABEL-SUM-3",
        lhs = "SUM(i, T, A) {DOT/MLTK/MLTB/MLTO} X (with side condition)",
        rhs = "SUM(i, T, A {DOT/MLTK/MLTB/MLTO} X)",
        rewrite_method = label_sum_3_rewrite
    )
    rules.append(LABEL_SUM_3)

    def label_sum_4_rewrite(rule, trs, term, side_info):
        if isinstance(term, ScalarDotL) and isinstance(term.args[1], SumS) or isinstance(term, (KetApplyL, BraApplyL, OpApplyL)) and isinstance(term.args[1], Sum):

            # we have to rename if necessary
            if set(v[0].name for v in term.args[1].bind_vars) & term.args[0].free_variables() == set():
                new_var = var_rename_ls(term.args[1].variables() | term.args[0].variables(), len(term.args[1].bind_vars))
                renamed_sum = term.args[1].rename_bind(tuple(TRSVar(v) for v in new_var))
            else:
                renamed_sum = term.args[1]

            combined_term = type(term)(term.args[0], renamed_sum.body)
            norm_term = trs.normalize(combined_term, **side_info['trs-args'])
            if norm_term != combined_term:
                if type(term) == ScalarDotL:
                    return SumS(renamed_sum.bind_vars, norm_term)
                else:
                    return Sum(renamed_sum.bind_vars, norm_term)
    LABEL_SUM_4 = TRSRule(
        "LABEL-SUM-4",
        lhs = "X {DOT/MLTK/MLTB/MLTO} SUM(i, T, A) (with side condition)",
        rhs = "SUM(i, T, X {DOT/MLTK/MLTB/MLTO} A)",
        rewrite_method = label_sum_4_rewrite
    )
    rules.append(LABEL_SUM_4)


    # def label_sum_5_rewrite(rule, trs, term, side_info):
    #     if isinstance(term, (KetTensorL, BraTensorL, OpOuterL, OpTensorL)) and isinstance(term.args[0], Sum):

    #         # we have to rename if necessary
    #         if set(v[0].name for v in term.args[0].bind_vars) & term.args[1].free_variables() == set():
    #             new_var = var_rename_ls(term.args[0].variables() | term.args[1].variables(), len(term.args[0].bind_vars))
    #             renamed_sum = term.args[0].rename_bind(tuple(TRSVar(v) for v in new_var))
    #         else:
    #             renamed_sum = term.args[0]

    #         combined_term = type(term)(renamed_sum.body, term.args[1])
    #         norm_term = trs.normalize(combined_term, **side_info['trs-args'])
    #         if norm_term != combined_term:
    #             return Sum(renamed_sum.bind_vars, norm_term)
    # LABEL_SUM_5 = TRSRule(
    #     "LABEL-SUM-5",
    #     lhs = "SUM(i, T, A) {TSRK/TSRB/OUTER/TSRO} X (with side condition)",
    #     rhs = "SUM(i, T, A {TSRK/TSRB/OUTER/TSRO} X)",
    #     rewrite_method = label_sum_5_rewrite
    # )
    # rules.append(LABEL_SUM_5)

    # def label_sum_6_rewrite(rule, trs, term, side_info):
    #     if isinstance(term, (KetTensorL, BraTensorL, OpOuterL, OpTensorL)) and isinstance(term.args[1], Sum):

    #         # we have to rename if necessary
    #         if set(v[0].name for v in term.args[1].bind_vars) & term.args[0].free_variables() == set():
    #             new_var = var_rename_ls(term.args[1].variables() | term.args[0].variables(), len(term.args[1].bind_vars))
    #             renamed_sum = term.args[1].rename_bind(tuple(TRSVar(v) for v in new_var))
    #         else:
    #             renamed_sum = term.args[1]

    #         combined_term = type(term)(term.args[0], renamed_sum.body)
    #         norm_term = trs.normalize(combined_term, **side_info['trs-args'])
    #         if norm_term != combined_term:
    #             return Sum(renamed_sum.bind_vars, norm_term)
    # LABEL_SUM_6 = TRSRule(
    #     "LABEL-SUM-6",
    #     lhs = "X {TSRK/TSRB/OUTER/TSRO} SUM(i, T, A) (with side condition)",
    #     rhs = "SUM(i, T, X {TSRK/TSRB/OUTER/TSRO} A)",
    #     rewrite_method = label_sum_6_rewrite
    # )
    # rules.append(LABEL_SUM_6)

    #############################################
    # temporary rules

    def label_temp_1_rewrite(rule, trs, term, side_info):
        if (isinstance(term, KetApplyL) and isinstance(term.args[1], KetTensorL) or isinstance(term, BraApplyL) and isinstance(term.args[1], OpTensorL) or isinstance(term, OpApplyL) and isinstance(term.args[1], OpTensorL)) and isinstance(term.args[0], Labelled1):
            for i, t in enumerate(term.args[1].args):
                if isinstance(t, Labelled1) and QReg.is_in(term.args[0].args[1], t.args[1]):
                    return type(term.args[1])(
                        type(term)(term.args[0], t),
                        *term.args[1].remained_terms(i)
                    )
    LABEL_TEMP_1 = TRSRule(
        "LABEL-TEMP-1",
        lhs = "A[R] {MLTO/MLTK/MLTB} (B[Q] TSRL X) (R is in Q)",
        rhs = "(A[R] {MLTO/MLTK/MLTB} B[Q]) TSRL X",
        rewrite_method = label_temp_1_rewrite
    )
    rules.append(LABEL_TEMP_1)


    LABEL_TEMP_1O = TRSRule(
        "LABEL-TEMP-1O",
        lhs = parse("A MLTOL (K[Q] OUTERL X)"),
        rhs = parse("(A MLTKL K[Q]) OUTERL X"),
    )
    rules.append(LABEL_TEMP_1O)

    def label_temp_1b_rewrite(rule, trs, term, side_info):
        if isinstance(term, BraApplyL) and isinstance(term.args[0], BraTensorL) and isinstance(term.args[1], OpOuterL) and isinstance(term.args[1].args[0], Labelled1):
            for i, t in enumerate(term.args[0].args):
                if isinstance(t, Labelled1) and t.args[1] == term.args[1].args[0].args[1]:
                    return ScalL(
                        ScalarDot(t.args[0], term.args[1].args[0].args[0]),
                        BraTensorL(
                            BraTensorL(*term.args[0].remained_terms(i)),
                            term.args[1].args[1]
                        )
                    )
    LABEL_TEMP_1B = TRSRule(
        "LABEL-TEMP-1B",
        lhs = "(Y TSRBL B[R]) MLTBL (K[R] OUTERL X)",
        rhs = "(B DOT K) SCRL (Y TSRBL X)",
        rewrite_method = label_temp_1b_rewrite
    )
    rules.append(LABEL_TEMP_1B)

    def label_temp_2_rewrite(rule, trs, term, side_info):
        if (isinstance(term, KetApplyL) and isinstance(term.args[0], OpTensorL) or isinstance(term, BraApplyL) and isinstance(term.args[0], BraTensorL) or isinstance(term, OpApplyL) and isinstance(term.args[0], OpTensorL)) and isinstance(term.args[1], Labelled1) :
            for i, t in enumerate(term.args[0].args):
                if isinstance(t, Labelled1) and QReg.is_in(term.args[1].args[1], t.args[1]):
                    return type(term.args[0])(
                        type(term)(t, term.args[1]),
                        *term.args[0].remained_terms(i)
                    )
    LABEL_TEMP_2 = TRSRule(
        "LABEL-TEMP-2",
        lhs = "(A[Q] TSRL X) {MLTO/MLTK/MLTB} B[R] (R is in Q)",
        rhs = "(A[Q] {MLTO/MLTK/MLTB} B[R]) TSRL X",
        rewrite_method = label_temp_2_rewrite
    )
    rules.append(LABEL_TEMP_2)


    LABEL_TEMP_2O = TRSRule(
        "LABEL-TEMP-2O",
        lhs = parse("(X OUTERL B[Q]) MLTOL A"),
        rhs = parse("X OUTERL (B[Q] MLTBL A)"),
    )
    rules.append(LABEL_TEMP_2O)

    def label_temp_2b_rewrite(rule, trs, term, side_info):
        if isinstance(term, KetApplyL) and isinstance(term.args[1], KetTensorL) and isinstance(term.args[0], OpOuterL) and isinstance(term.args[0].args[1], Labelled1):
            for i, t in enumerate(term.args[1].args):
                if isinstance(t, Labelled1) and t.args[1] == term.args[0].args[1].args[1]:
                    return ScalL(
                        ScalarDot(term.args[0].args[1].args[0], t.args[0]),
                        KetTensorL(
                            term.args[0].args[0],
                            KetTensorL(*term.args[1].remained_terms(i))
                        )
                    )
    LABEL_TEMP_2B = TRSRule(
        "LABEL-TEMP-2B",
        lhs = "(X OUTERL B[R]) MLTKL (K[R] TSRKL Y)",
        rhs = "(B DOT K) SCRL (X TSRKL Y)",
        rewrite_method = label_temp_2b_rewrite
    )
    rules.append(LABEL_TEMP_2B)

    def label_temp_3_rewrite(rule, trs, term, side_info):
        if isinstance(term, ScalarDot) and isinstance(term.args[0], Labelled1) and isinstance(term.args[1], KetTensorL):
            for i, t in enumerate(term.args[1].args):
                if isinstance(t, Labelled1) and t.args[1] == term.args[0].args[1]:
                    return Scal(
                        ScalarDot(term.args[0], t),
                        KetTensorL(*term.args[1].remained_terms(i))
                    )
    LABEL_TEMP_3 = TRSRule(
        "LABEL-TEMP-3",
        lhs = "A[R] DOT (B[R] TSRL X)",
        rhs = "(A[R] DOT B[R]) SCR X",
        rewrite_method = label_temp_3_rewrite
    )
    rules.append(LABEL_TEMP_3)


    def label_temp_4_rewrite(rule, trs, term, side_info):
        if isinstance(term, ScalarDot) and isinstance(term.args[1], Labelled1) and isinstance(term.args[0], BraTensorL):
            for i, t in enumerate(term.args[0].args):
                if isinstance(t, Labelled1) and t.args[1] == term.args[1].args[1]:
                    return Scal(
                        ScalarDot(t, term.args[1]),
                        BraTensorL(*term.args[0].remained_terms(i))
                    )
    LABEL_TEMP_4 = TRSRule(
        "LABEL-TEMP-4",
        lhs = "(A[R] TSRL X) DOT B[R]",
        rhs = "(A[R] DOT B[R]) SCR X",
        rewrite_method = label_temp_4_rewrite
    )
    rules.append(LABEL_TEMP_4)


    # build the trs
    return TRS(rules)