
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
            mma_vars = side_info['mma_vars']
            if mma_vars == ():
                if term.args[0][0] != term.args[1][0]:
                    return C0
            else:
                if not term.args[0][0].eq_satisfiable(term.args[1][0], mma_vars):
                    return C0
    
    DELTA_AST_2 = TRSRule(
        lhs = "DELTA(s, t) && s, t are base atoms && s = t is not satisfiable",
        rhs = "C(0)",
        rewrite_method=delta_ast_2_rewrite
    )
    rules.append(DELTA_AST_2)


    # define the preprocess of side information

    def side_info_vars_proc(side_info: dict[str, Any]) -> dict[str, Any]:
        if "mma_vars" not in side_info:
            side_info["mma_vars"] = ()
            return side_info
        
        else:
            if isinstance(side_info["mma_vars"], str):
                side_info["mma_vars"] = wolfram_backend.session.evaluate(side_info["mma_vars"])
            return side_info


    # construct the trs
    return TRS(rules, trs.side_info_procs + (side_info_vars_proc,))


