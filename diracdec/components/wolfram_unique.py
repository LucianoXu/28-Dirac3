'''
The implementation for complex scalar system by wolfram expressions

This is the "unique" version. The backend will maintain a table of existing expressions to ensure that semantically equivalent expressions only have one instance.

Semantical equivalence is checked by testing `FullSimplify[A == B]`
'''

from __future__ import annotations
from typing import Any, List

from diracdec.theory.trs import Subst, Term, StdTerm, BindVarTerm

from ..theory.atomic_base import AtomicBase
from ..theory.complex_scalar import ComplexScalar

from ..theory import Term, Var, Subst

from ..backends.wolfram_backend import *

# introduce transformations from simple Wolfram backend
from .wolfram_simple import WolframABase, WolframCScalar

import hashlib

class WolABaseUnique(AtomicBase):

    # this list of all complex scalars constructed
    table : set[WolABaseUnique] = set()

    def __new__(cls, expr : str | Any):
        '''
        return the unique instance equivalent to expr
        '''

        if isinstance(expr, str):
            expr = wlexpr(expr)

        # search for the existing expressions
        for instance in WolABaseUnique.table:
            if session.evaluate(wl.FullSimplify(wl.Equal(instance.expr, expr))) == True:
                return instance
            
        # simplify, append the new instance in the table
        expr = session.evaluate(wl.FullSimplify(expr))
        obj = object.__new__(cls)
        obj.expr = expr
        WolABaseUnique.table.add(obj)
        return obj
        
    def __init__(self, expr : str | Any):
        self.expr : Any


    def __str__(self) -> str:
        return str(session.evaluate(wl.ToString(self.expr)))
    
    def __repr__(self) -> str:
        return f'WolABaseUnique({self.expr})'
    
    def tex(self) -> str:
        return session.evaluate(wl.ToString(self.expr, wl.TeXForm))    
    
    def __eq__(self, other: WolABaseUnique) -> bool:
        return self is other
        
    def __hash__(self) -> int:
        h = hashlib.md5(str(self.expr).encode())
        return int(h.hexdigest(), 16)
    
    def size(self) -> int:
        return 1
    

    def variables(self) -> set[Var]:
        '''
        Special symbols like "Inifinity" will also match _Symbol, and we rule them out.

        Notice: the "Global`" prefix is removed
        '''
        return set(Var(v.name.replace("Global`", ""))
                   for v in session.evaluate(wl.Cases(wl.List(self.expr), wl.Blank(wl.Symbol), wl.Infinity)) 
                   if isinstance(v, WLSymbol)
                   )

    def eq_satisfiable(self, other) -> bool:
        '''
        check whether e1 == e2 is satisfiable with variables of [vars]
        vars is the MMA list of variables
        '''
        common_vars = self.variables() | other.variables()

        if common_vars == set():
            return self is other
        
        else:
            vars = wl.List(*[wl.Symbol(v.name) for v in common_vars])
            res = session.evaluate(wl.FindInstance(wl.Equal(self.expr, other.expr), vars))
            return res != ()
        
    def subst(self, sigma: Subst | dict[Var, Term]) -> Term:

        if not isinstance(sigma, Subst):
            sigma = Subst(sigma)

        # create the substitution in Wolfram Language
        wolfram_sub = []
        for k, v in sigma.data.items():
            if isinstance(v, Var):
                wolfram_sub.append(wl.Rule(wl.Symbol(k.name), wl.Symbol(v.name)))
            elif isinstance(v, WolABaseUnique) or isinstance(v, WolCScalarUnique):
                wolfram_sub.append(wl.Rule(wl.Symbol(k.name), v.expr))
        if len(wolfram_sub) == 0:
            return self

        # substitute
        return WolABaseUnique(wl.ReplaceAll(self.expr, tuple(wolfram_sub)))
    
    def reduce(self) -> WolABaseUnique | None:
        if isinstance(self.expr, WLFunction) and self.expr.head == wl.HoldForm:
            return WolABaseUnique(self.expr[0])
        else:
            return None
        


class WolCScalarUnique(ComplexScalar):

    # this list of all complex scalars constructed
    table : set[WolCScalarUnique] = set()

    def __new__(cls, expr : str | Any):
        '''
        return the unique instance equivalent to expr
        '''

        if isinstance(expr, str):
            expr = wlexpr(expr)

        # search for the existing expressions
        for instance in WolCScalarUnique.table:
            if session.evaluate(wl.FullSimplify(wl.Equal(instance.expr, expr))) == True:
                return instance
            
        # simplify, append the new instance in the table
        expr = session.evaluate(wl.FullSimplify(expr))
        obj = object.__new__(cls)
        obj.expr = expr
        WolCScalarUnique.table.add(obj)
        return obj
        
    def __init__(self, expr : str | Any):
        self.expr : Any


    @staticmethod
    def zero() -> WolCScalarUnique:
        return WolCScalarUnique("0")
    
    @staticmethod
    def one() -> WolCScalarUnique:
        return WolCScalarUnique("1")
    
    @staticmethod
    def conj(c : WolCScalarUnique) -> WolCScalarUnique:
        return WolCScalarUnique(wl.Conjugate(c.expr))
    
    @staticmethod
    def add(c1 : WolCScalarUnique, c2 : WolCScalarUnique) -> WolCScalarUnique:
        return WolCScalarUnique(wl.Plus(c1.expr, c2.expr))
    
    @staticmethod
    def mlt(c1 : WolCScalarUnique, c2 : WolCScalarUnique) -> WolCScalarUnique:
        return WolCScalarUnique(wl.Times(c1.expr, c2.expr))
    
    def __str__(self) -> str:
        return str(session.evaluate(wl.ToString(self.expr)))
    
    def __repr__(self) -> str:
        return f'WolCScalarUnique({self.expr})'
    
    def tex(self) -> str:
        return r"\left (" + session.evaluate(wl.ToString(self.expr, wl.TeXForm)) + r"\right )"
    
    def __eq__(self, other: WolCScalarUnique) -> bool:
        return self is other
    
    def __hash__(self) -> int:
        h = hashlib.md5(str(self.expr).encode())
        return int(h.hexdigest(), 16)
    
    def size(self) -> int:
        return 1
    
    def variables(self) -> set[Var]:
        '''
        Special symbols like "Inifinity" will also match _Symbol, and we rule them out.
        '''
        return set(Var(v.name.replace("Global`", ""))
                   for v in session.evaluate(wl.Cases(wl.List(self.expr), wl.Blank(wl.Symbol), wl.Infinity)) 
                   if isinstance(v, WLSymbol)
                   )

    def subst(self, sigma: Subst | dict[Var, Term]) -> Term:

        if not isinstance(sigma, Subst):
            sigma = Subst(sigma)

        # create the substitution in Wolfram Language
        wolfram_sub = []
        for k, v in sigma.data.items():
            if isinstance(v, Var):
                wolfram_sub.append(wl.Rule(wl.Symbol(k.name), wl.Symbol(v.name)))
            elif isinstance(v, WolCScalarUnique) or isinstance(v, WolABaseUnique):
                wolfram_sub.append(wl.Rule(wl.Symbol(k.name), v.expr))
        if len(wolfram_sub) == 0:
            return self

        # substitute
        return WolCScalarUnique(wl.ReplaceAll(self.expr, tuple(wolfram_sub)))
    
    def reduce(self) -> WolCScalarUnique | None:
        if isinstance(self.expr, WLFunction) and self.expr.head == wl.HoldForm:
            return WolCScalarUnique(self.expr[0])
        else:
            return None
        
def wolU(term : Term) -> Term:
    '''
    iteratively transform all simple Wolfram backend instances to the unique version
    '''
    if isinstance(term, WolframABase):
        return WolABaseUnique(term.simp_expr)
    
    elif isinstance(term, WolframCScalar):
        return WolCScalarUnique(term.simp_expr)
    
    elif isinstance(term, StdTerm):
        return type(term)(*map(wolU, term.args))
    
    elif isinstance(term, BindVarTerm):
        return type(term)(term.bind_var, wolU(term.body))
    
    else:
        return term
