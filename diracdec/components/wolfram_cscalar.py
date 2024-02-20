'''
The implementation for complex scalar system by python floating point numbers
'''

from __future__ import annotations

from typing import Any

from ..theory.complex_scalar import ComplexScalar

from ..backends.wolfram_backend import *

import hashlib

class WolframCScalar(ComplexScalar):
    def __init__(self, expr : str | Any):

        if isinstance(expr, str):
            expr = wlexpr(expr)

        self.simp_expr = session.evaluate(wl.FullSimplify(expr))

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
        return f'{str(self.simp_expr)}'
    
    def __repr__(self) -> str:
        return f'WolframCScalar({self.simp_expr})'
    
    def __eq__(self, other: WolframCScalar) -> bool:
        return isinstance(other, WolframCScalar) and self.simp_expr == other.simp_expr
    
    def __hash__(self) -> int:
        h = hashlib.md5(str(self).encode())
        return int(h.hexdigest(), 16)
