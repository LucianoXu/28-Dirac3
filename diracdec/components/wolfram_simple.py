'''
The implementation for complex scalar system by wolfram expressions
'''

from __future__ import annotations
from typing import Any

from diracdec.theory.trs import Subst, TRSTerm

from ..theory.atomic_base import AtomicBase
from ..theory.complex_scalar import ComplexScalar

from ..theory import TRSTerm, TRSVar, Subst

from ..backends.wolfram_backend import *

import hashlib

class WolframABase(AtomicBase):
    def __init__(self, expr : str | Any):

        if isinstance(expr, str):
            expr = wlexpr(expr)

        self.simp_expr = session.evaluate(wl.FullSimplify(expr))
        
        TRSTerm.__init__(self)

    def __str__(self) -> str:
        return str(session.evaluate(wl.ToString(self.simp_expr)))
    
    def __repr__(self) -> str:
        return f'WolframABase({self.simp_expr})'
    
    def tex(self) -> str:
        return session.evaluate(wl.ToString(self.simp_expr, wl.TeXForm))    
    
    def __eq__(self, other: WolframABase) -> bool:
        return isinstance(other, WolframABase) and self.simp_expr == other.simp_expr
    
    def __hash__(self) -> int:
        h = hashlib.md5(str(self.simp_expr).encode())
        return int(h.hexdigest(), 16)
    
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
            if isinstance(v, TRSVar):
                wolfram_sub.append(wl.Rule(wl.Symbol(k), wl.Symbol(v.name)))
            elif isinstance(v, WolframABase) or isinstance(v, WolframCScalar):
                wolfram_sub.append(wl.Rule(wl.Symbol(k), v.simp_expr))
        if len(wolfram_sub) == 0:
            return self

        # substitute
        return WolframABase(wl.ReplaceAll(self.simp_expr, tuple(wolfram_sub)))
    
    def reduce(self) -> WolframABase | None:
        if isinstance(self.simp_expr, WLFunction) and self.simp_expr.head == wl.HoldForm:
            return WolframABase(self.simp_expr[0])
        else:
            return None
        


class WolframCScalar(ComplexScalar):
    def __init__(self, expr : str | Any):

        if isinstance(expr, str):
            expr = wlexpr(expr)

        self.simp_expr = session.evaluate(wl.FullSimplify(expr))

        TRSTerm.__init__(self)

    @staticmethod
    def zero() -> WolframCScalar:
        return WolframCScalar("0")
    
    @staticmethod
    def one() -> WolframCScalar:
        return WolframCScalar("1")
    
    @staticmethod
    def conj(c : WolframCScalar) -> WolframCScalar:
        return WolframCScalar(wl.Conjugate(c.simp_expr))
    
    @staticmethod
    def add(c1 : WolframCScalar, c2 : WolframCScalar) -> WolframCScalar:
        return WolframCScalar(wl.Plus(c1.simp_expr, c2.simp_expr))
    
    @staticmethod
    def mlt(c1 : WolframCScalar, c2 : WolframCScalar) -> WolframCScalar:
        return WolframCScalar(wl.Times(c1.simp_expr, c2.simp_expr))
    
    def __str__(self) -> str:
        return str(session.evaluate(wl.ToString(self.simp_expr)))
    
    def __repr__(self) -> str:
        return f'WolframCScalar({self.simp_expr})'
    
    def tex(self) -> str:
        return r"\left (" + session.evaluate(wl.ToString(self.simp_expr, wl.TeXForm)) + r"\right )"
    
    def __eq__(self, other: WolframCScalar) -> bool:
        return isinstance(other, WolframCScalar) and self.simp_expr == other.simp_expr
    
    def __hash__(self) -> int:
        h = hashlib.md5(str(self.simp_expr).encode())
        return int(h.hexdigest(), 16)
    
    def size(self) -> int:
        return 1
    
    def variables(self) -> set[str]:
        '''
        Special symbols like "Inifinity" will also match _Symbol, and we rule them out.
        '''
        return set(v.name.replace("Global`", "") 
                   for v in session.evaluate(wl.Cases(self.simp_expr, wl.Blank(wl.Symbol), wl.Infinity)) 
                   if isinstance(v, WLSymbol)
                   )

    def substitute(self, sigma: Subst) -> TRSTerm:
        # create the substitution in Wolfram Language
        wolfram_sub = []
        for k, v in sigma.data.items():
            if isinstance(v, TRSVar):
                wolfram_sub.append(wl.Rule(wl.Symbol(k), wl.Symbol(v.name)))
            elif isinstance(v, WolframCScalar) or isinstance(v, WolframABase):
                wolfram_sub.append(wl.Rule(wl.Symbol(k), v.simp_expr))
        if len(wolfram_sub) == 0:
            return self

        # substitute
        return WolframCScalar(wl.ReplaceAll(self.simp_expr, tuple(wolfram_sub)))
    
    def reduce(self) -> WolframCScalar | None:
        if isinstance(self.simp_expr, WLFunction) and self.simp_expr.head == wl.HoldForm:
            return WolframCScalar(self.simp_expr[0])
        else:
            return None