'''
The implementation for complex scalar system by python floating point numbers
'''

from __future__ import annotations

from typing import Any

from ..theory.complex_scalar import ComplexScalar

from ..theory import TRSTerm, Subst

from ..backends.wolfram_backend import *

import hashlib

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
        return f'\n{str(session.evaluate(wl.ToString(self.simp_expr)))}\n'
    
    def __repr__(self) -> str:
        return f'WolframCScalar({self.simp_expr})'
    
    def tex(self) -> str:
        return r"\left (" + session.evaluate(wl.ToString(self.simp_expr, wl.TeXForm)) + r"\right )"
    
    def __eq__(self, other: WolframCScalar) -> bool:
        return isinstance(other, WolframCScalar) and self.simp_expr == other.simp_expr
    
    def __hash__(self) -> int:
        h = hashlib.md5(str(self.simp_expr).encode())
        return int(h.hexdigest(), 16)
    
    def variables(self) -> set[str]:
        return set(v.name for v in session.evaluate(wl.Cases(self.simp_expr, wl.Blank(wl.Symbol), wl.Infinity)))

    def substitute(self, sigma: Subst) -> TRSTerm:
        # create the substitution in Wolfram Language
        wolfram_sub = []
        for k, v in sigma.data.items():
            if isinstance(v, WolframCScalar):
                wolfram_sub.append(wl.Rule(wl.Symbol(k), v.simp_expr))
        if len(wolfram_sub) == 0:
            return self

        # substitute
        return WolframCScalar(session.evaluate(wl.ReplaceAll(self.simp_expr, tuple(wolfram_sub))))