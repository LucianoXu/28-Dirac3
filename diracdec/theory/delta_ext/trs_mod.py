
from __future__ import annotations

from typing import Type

from ply import yacc

from ..trs import *

from ..dirac import *

from ..atomic_base import AtomicBase
from ..complex_scalar import ComplexScalar

from ...backends import wolfram_backend

def modify_trs(
        trs: TRS, 
        CScalar: Type[ComplexScalar], 
        ABase: Type[AtomicBase]) -> TRS:
    '''
    return a new trs with modified terms
    (the original trs is not modified)
    '''

    C0 = ScalarC(CScalar.zero())
    C1 = ScalarC(CScalar.one())

    rules = trs.rules.copy()

    #########################################
    # extra rules for delta
    def delta_ast_1_rewrite(rule, term, side_info):
        if isinstance(term, ScalarDelta):
            if term.args[0] == term.args[1]:
                return C1
            
    DELTA_AST_1 = TRSRule(
        lhs = "DELTA(s, s)",
        rhs = "C(1)",
        rewrite_method=delta_ast_1_rewrite
    )
    rules.append(DELTA_AST_1)


    def delta_ast_2_rewrite(rule, term, side_info):
        if isinstance(term, ScalarDelta) and isinstance(term[0], BaseAtom) and isinstance(term[1], BaseAtom):
            if not term.args[0][0].eq_satisfiable(term.args[1][0]): # type: ignore
                return C0
    
    DELTA_AST_2 = TRSRule(
        lhs = "DELTA(s, t) && s, t are base atoms && s = t is not satisfiable",
        rhs = "C(0)",
        rewrite_method=delta_ast_2_rewrite
    )
    rules.append(DELTA_AST_2)


    # construct the trs
    return TRS(rules, trs.side_info_procs)


