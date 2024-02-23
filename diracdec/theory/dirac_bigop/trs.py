

from __future__ import annotations

from typing import Type

from ply import yacc


from ..trs import *
from .syntax import *
from ..atomic_base import AtomicBase
from ..complex_scalar import ComplexScalar

from .parser import construct_parser

from ..dirac.trs import construct_trs as dirac_construct_trs

def construct_trs(
        CScalar: Type[ComplexScalar], 
        ABase: Type[AtomicBase], 
        parser: yacc.LRParser|None = None) -> TRS:

    # construct the parser
    if parser is None:
        parser = construct_parser(CScalar, ABase)

    def parse(s: str) -> TRSTerm:
        return parser.parse(s)
    
    # inherit the rules from dirac
    dirac_trs = dirac_construct_trs(CScalar, ABase)
    rules = dirac_trs.rules.copy()

    #####################################################
    # beta-reduction

    def beta_reduction_rewrite(rule, term, side_info):
        if isinstance(term, Apply):
            f, x = term.args
            if isinstance(f, Abstract):
                return f.body.substitute(Subst({f.bind_var.name: x}))
            
    BETA_REDUCTION = TRSRule(
        "BETA_REDUCTION",
        lhs = "APPLY(LAMBDA(x, A), a)",
        rhs = "A[x := a]",
        rewrite_method = beta_reduction_rewrite,
        rule_repr = "(* beta-reduction: APPLY(LAMBDA(x, A), a) -> A[x := a] ;*)",
    )
    rules.append(BETA_REDUCTION)

    # build the trs
    return TRS(rules)