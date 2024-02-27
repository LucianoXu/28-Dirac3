
from ..dirac.syntax import *

from ..trs import BindVarTerm


#####################################
# transpose

class KetTrans(DiracKet, StdTerm):
    fsymbol_print = "TRANK"
    fsymbol = "TRANK"

    def __init__(self, B : TRSTerm):
        super().__init__(B)

    def __str__(self) -> str:
        return f"({self.args[0]}^T)"
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^T"
    
class BraTrans(DiracBra, StdTerm):
    fsymbol_print = "TRANB"
    fsymbol = "TRANB"

    def __init__(self, K : TRSTerm):
        super().__init__(K)

    def __str__(self) -> str:
        return f"({self.args[0]}^T)"
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^T"
    
class OpTrans(DiracOp, StdTerm):
    fsymbol_print = "TRANO"
    fsymbol = "TRANO"

    def __init__(self, O : TRSTerm):
        super().__init__(O)

    def __str__(self) -> str:
        return f"({self.args[0]}^T)"
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^T"



#####################################
# high-level constructions


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
    

#####################################
# section-2 syntax
    
class Juxtapose(DiracScalar, TRSCommBinary):
    '''
    Note: this rule is only for internal representation, and should not be used in the user interface or parsing
    '''
    fsymbol_print = "JUXT"
    fsymbol = "JUXT"

    def __init__(self, A: TRSTerm, B: TRSTerm):
        super().__init__(A, B)

    def __str__(self) -> str:
        '''
        use the first one to represent
        '''
        return str(self.args[0])
    
    def tex(self) -> str:
        '''
        use the first one to represent
        '''
        return self.args[0].tex()
    
class SumEq(TRS_AC):
    '''
    Note: this rule is only for internal representation, and should not be used in the user interface or parsing
    '''
    fsymbol_print = "SUMEQ"
    fsymbol = "SUMEQ"

    def __init__(self, *tup : TRSTerm):
        TRS_AC.__init__(self, *tup)

    def __str__(self) -> str:
        '''
        use the first one to represent
        '''
        return str(self.args[0])
    
    def tex(self) -> str:
        '''
        use the first one to represent
        '''
        return self.args[0].tex()




