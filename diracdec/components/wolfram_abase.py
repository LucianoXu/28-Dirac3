'''
The implementation for complex scalar system by wolfram expressions
'''

from __future__ import annotations

from ..theory.atomic_base import AtomicBase

from ..backends.wolfram_backend import *



class WolframABase(AtomicBase):
    def __init__(self, expr : str):
        self.simp_expr = wolfram_parser(f"FullSimplify[{expr}]")

    def __str__(self) -> str:
        return str(self.simp_expr)
    
    def __repr__(self) -> str:
        return f'WolframABase({self.simp_expr})"'
    
    def __eq__(self, other: WolframABase) -> bool:
        return isinstance(other, WolframABase) and self.simp_expr == other.simp_expr
    
    def __hash__(self) -> int:
        return hash(self.simp_expr)

    def eq_satisfiable(self, other, vars) -> bool:
        '''
        check whether e1 == e2 is satisfiable with variables of [vars]
        vars is the MMA list of variables
        '''
        res = session.evaluate(wl.FindInstance(wl.Equal(self.simp_expr, other.simp_expr), vars))
        return res != ()