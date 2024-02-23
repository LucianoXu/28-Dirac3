'''
The implementation for complex scalar system by wolfram expressions
'''

from __future__ import annotations
from typing import Any

from diracdec.theory.trs import Subst, TRSTerm

from ..theory.atomic_base import AtomicBase

from ..theory import TRSTerm, Subst

from ..backends.wolfram_backend import *



class WolframABase(AtomicBase):
    def __init__(self, expr : str | Any):

        if isinstance(expr, str):
            expr = wlexpr(expr)

        self.simp_expr = session.evaluate(wl.FullSimplify(expr))
        
        TRSTerm.__init__(self)

    def __str__(self) -> str:
        return str(self.simp_expr)
    
    def __repr__(self) -> str:
        return f'WolframABase({self.simp_expr})"'
    
    def tex(self) -> str:
        return session.evaluate(wl.ToString(self.simp_expr, wl.TeXForm))    
    
    def __eq__(self, other: WolframABase) -> bool:
        return isinstance(other, WolframABase) and self.simp_expr == other.simp_expr
    
    def __hash__(self) -> int:
        return hash(self.simp_expr)
    
    def size(self) -> int:
        return 1
    

    def variables(self) -> set[str]:
        '''
        Special symbols like "Inifinity" will also match _Symbol, and we rule them out.

        Notice: the "Global`" prefix is removed
        '''
        return set(v.name.replace("Global`", "") 
                   for v in session.evaluate(wl.Cases(self.simp_expr, wl.Blank(wl.Symbol), wl.Infinity)) 
                   if isinstance(v, WLSymbol)
                   )

    def eq_satisfiable(self, other) -> bool:
        '''
        check whether e1 == e2 is satisfiable with variables of [vars]
        vars is the MMA list of variables
        '''
        common_vars = self.variables() | other.variables()

        if common_vars == set():
            return self.simp_expr == other.simp_expr
        
        else:
            vars = wl.List(*[wl.Symbol(v) for v in common_vars])
            res = session.evaluate(wl.FindInstance(wl.Equal(self.simp_expr, other.simp_expr), vars))
            return res != ()
        
    def substitute(self, sigma: Subst) -> TRSTerm:

        # create the substitution in Wolfram Language
        wolfram_sub = []
        for k, v in sigma.data.items():
            if isinstance(v, WolframABase):
                wolfram_sub.append(wl.Rule(wl.Symbol(k), v.simp_expr))
        if len(wolfram_sub) == 0:
            return self

        # substitute
        return WolframABase(session.evaluate(wl.ReplaceAll(self.simp_expr, tuple(wolfram_sub))))
    
    def reduce(self) -> WolframABase | None:
        if isinstance(self.simp_expr, WLFunction) and self.simp_expr.head == wl.HoldForm:
            return WolframABase(self.simp_expr[0])
        else:
            return None