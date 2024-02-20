
'''
all the rewriting rules for Dirac notation
'''

from __future__ import annotations
from .theory.trs import *
from .theory.dirac_syntax import *

from .components.py_cscalar import PyCScalar

rules = []

CScalar = PyCScalar
C0 = ScalarC(CScalar.zero())
C1 = ScalarC(CScalar.one())
C2 = ScalarC(CScalar.add(CScalar.one(), CScalar.one()))

# class class_SCR_COMPLEX_1(TRSRule):
    

def scr_complex_1_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            if term.args[i] == C0:
                return ScalarAdd(*term.remained_terms(i))

SCR_COMPLEX_1 = TRSRule(
    lhs="C(0) ADDS a", 
    rhs="a",
    rewrite_method=scr_complex_1_rewrite
)
rules.append(SCR_COMPLEX_1)


def scr_complex_2_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            if isinstance(term.args[i], ScalarC):
                for j in range(i+1, len(term.args)):
                    if isinstance(term.args[j], ScalarC):

                        new_args = (ScalarC(CScalar.add(term.args[i].args[0], term.args[j].args[0])),) + term.remained_terms(i, j)

                        return ScalarAdd(*new_args)

SCR_COMPLEX_2 = TRSRule(
    lhs="C(a) ADDS C(b)", 
    rhs="C(a + b)",
    rewrite_method=scr_complex_2_rewrite
)
rules.append(SCR_COMPLEX_2)

def scr_complex_3_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            for j in range(i+1, len(term.args)):
                if term.args[i] == term.args[j]:
                    new_args = (ScalarMlt(C2, term.args[i]),) + term.remained_terms(i, j)
                    return ScalarAdd(*new_args)
                
SCR_COMPLEX_3 = TRSRule(
    lhs = "S0 ADDS S0",
    rhs = "C(1 + 1) MLTS S0",
    rewrite_method=scr_complex_3_rewrite
)
rules.append(SCR_COMPLEX_3)

def scr_complex_4_rewrite(rule, term):
    if isinstance(term, ScalarAdd):
        for i in range(len(term.args)):
            if isinstance(term.args[i], ScalarMlt):
                for j in range(len(term.args[i].args)):
                    if isinstance(term[i][j], ScalarC):
                        new_args = (*term[i].args[:j], *term[i].args[j+1:])
                        if len(new_args) == 1:
                            S0 = new_args[0]
                        else:
                            S0 = ScalarMlt(*term[i].args[:j], *term[i].args[j+1:])
                            
                        for k in range(len(term.args)):
                            if S0 == term.args[k]:
                                new_args = (ScalarMlt(ScalarC(CScalar.add(term[i][j].args[0], CScalar.one())), term[k]),)
                                i, k = min(i, k), max(i, k)
                                new_args += term.args[:i] + term.args[i+1:k] + term.args[k+1:]
                                return ScalarAdd(*new_args)
                                
SCR_COMPLEX_4 = TRSRule(
    lhs = "(C(a) MLTS S0) ADDS S0",
    rhs = "C(a + 1) MLTS S0",
    rewrite_method=scr_complex_4_rewrite
)
rules.append(SCR_COMPLEX_4)



SCR_COMPLEX_1a = TRSRule(
    lhs=ScalarConj(ScalarConj(TRSVar("?S"))), 
    rhs=TRSVar("?S")
)
rules.append(SCR_COMPLEX_1a)

diractrs = TRS(rules)