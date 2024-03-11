
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
        lhs = parse("RFST(RPAIR(s, t))"),
        rhs = parse("s")
    )
    rules.append(REG_1)

    REG_2 = TRSRule(
        "REG-2",
        lhs = parse("RSND(RPAIR(s, t))"),
        rhs = parse("t")
    )
    rules.append(REG_2)

    REG_3 = TRSRule(
        "REG-3",
        lhs = parse("RPAIR(RFST(s), RSND(s))"),
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

    # build the trs
    return TRS(rules)
