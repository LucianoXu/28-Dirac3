
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
        if isinstance(term, AddL):
            for i in range(len(term.args)):
                ti = term.args[i]
                if isinstance(ti, Labelled1):
                    for j in range(i + 1, len(term.args)):
                        tj = term.args[j]
                        if isinstance(tj, Labelled1) and ti.args[1] == tj.args[1]:
                            return AddL(
                                Labelled1(Add(ti.args[0], tj.args[0]), ti.args[1]),
                                *term.remained_terms(i, j))
    LABEL_LIFT_5 = TRSRule(
        "LABEL-LIFT-5",
        lhs = " (A[R]) ADDL (B[R]) ",
        rhs = " (A ADD B)[R] ",
        rewrite_method = label_lift_5_rewrite
    )
    rules.append(LABEL_LIFT_5)

    def label_lift_6_rewrite(rule, trs, term, side_info):
        if isinstance(term, AddL):
            for i in range(len(term.args)):
                ti = term.args[i]
                if isinstance(ti, Labelled2):
                    for j in range(i + 1, len(term.args)):
                        tj = term.args[j]
                        if isinstance(tj, Labelled2) and ti.args[1] == tj.args[1] and ti.args[2] == tj.args[2]:
                            return AddL(
                                Labelled2(Add(ti.args[0], tj.args[0]), ti.args[1], ti.args[2]),
                                *term.remained_terms(i, j))
    LABEL_LIFT_6 = TRSRule(
        "LABEL-LIFT-6",
        lhs = " (A[Q; R]) ADDL (B[Q; R]) ",
        rhs = " (A ADD B)[Q; R] ",
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

    LABEL_LIFT_15 = TRSRule(
        "LABEL-LIFT-15",
        lhs = parse(''' (A[R]) MLTOL (B[R]) '''),
        rhs = parse(''' (A MLTO B)[R] ''')
    )
    rules.append(LABEL_LIFT_15)


    LABEL_LIFT_16 = TRSRule(
        "LABEL-LIFT-16",
        lhs = parse(''' (A[R]) DOTL (B[R]) '''),
        rhs = parse(''' A DOT B ''')
    )
    rules.append(LABEL_LIFT_16)

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
        if isinstance(term, Sum) and isinstance(term.body, Labelled1):
            return Labelled1(Sum(term.bind_vars, term.body.args[0]), term.body.args[1])
    LABEL_SUM_1 = TRSRule(
        "LABEL-SUM-1",
        lhs = " SUM(x, T, A[R]) ",
        rhs = " SUM(x, T, A)[R] ",
        rewrite_method = label_sum_1_rewrite
    )
    rules.append(LABEL_SUM_1)


    def label_sum_2_rewrite(rule, trs, term, side_info):
        if isinstance(term, Sum) and isinstance(term.body, Labelled2):
            return Labelled2(Sum(term.bind_vars, term.body.args[0]), term.body.args[1], term.body.args[2])
    LABEL_SUM_2 = TRSRule(
        "LABEL-SUM-2",
        lhs = " SUM(x, T, A[Q; R]) ",
        rhs = " SUM(x, T, A)[Q; R] ",
        rewrite_method = label_sum_2_rewrite
    )
    rules.append(LABEL_SUM_2)


    # build the trs
    return TRS(rules)
