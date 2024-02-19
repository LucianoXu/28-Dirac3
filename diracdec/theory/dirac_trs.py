
'''
all the rewriting rules for Dirac notation
'''

from __future__ import annotations
from .trs import *
from .dirac_syntax import *

from ..components.py_cscalar import PyCScalar

rules = []

CScalar = PyCScalar
C0 = ScalarC(CScalar.zero())

# class class_SCR_COMPLEX_1(TRSRule):
    

def scr_complex_1_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            if term.args[i] == C0:
                new_args = term.args[:i] + term.args[i+1:]
                if len(new_args) == 1:
                    return new_args[0]
                else:
                    return type(term)(new_args)
    
    return None
        
    
SCR_COMPLEX_1 = TRSRule(
    lhs=ScalarAdd((ScalarC(CScalar.zero()), TRSVar("?S"))), 
    rhs=TRSVar("?S"),
    rewrite_method=scr_complex_1_rewrite
)
rules.append(SCR_COMPLEX_1)

SCR_COMPLEX_1a = TRSRule(
    lhs=ScalarConj(ScalarConj(TRSVar("?S"))), 
    rhs=TRSVar("?S")
)
rules.append(SCR_COMPLEX_1a)

diractrs = TRS(rules)