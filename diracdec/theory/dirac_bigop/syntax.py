
from ..dirac.syntax import *

from ..trs import BindVarTerm

class Abstract(BindVarTerm):
    fsymbol_print = "λ"
    fsymbol = "LAMBDA"

    def tex(self) -> str:
        return rf" \left ( \lambda {self.bind_var.name} . {self.body.tex()} \right )"
    
class Apply(StdTerm):
    fsymbol_print = "apply"
    fsymbol = "APPLY"

    def __init__(self, f: TRSTerm, x: TRSTerm):
        super().__init__(f, x)

    def tex(self) -> str:
        return rf" \left ({self.args[0].tex()} {self.args[1].tex()} \right)"

class ScalarSum(DiracScalar, BindVarTerm):
    fsymbol_print = "sum"
    fsymbol = "SUMS"

    def tex(self) -> str:
        return rf" \left ( \sum_{{{self.bind_var.name}}} {self.body.tex()} \right )"