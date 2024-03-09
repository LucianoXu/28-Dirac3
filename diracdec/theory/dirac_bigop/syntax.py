from ..dirac.syntax import *

from ..trs import BindVarTerm, MultiBindTerm

#####################################
# transpose

class Transpose(DiracNotation, StdTerm):
    fsymbol_print = "TP"
    fsymbol = "TP"

    def __init__(self, X : TRSTerm):
        super().__init__(X)

    def __str__(self) -> str:
        return str(IndexBlock(str(self.args[0]), UR_index="⊤"))
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^\top"
    
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

    def __str__(self) -> str:
        return str(HSeqBlock(
            str(self.args[0]), ' ', str(self.args[1]), 
            v_align='c'))

    def tex(self) -> str:
        return rf" \left ({self.args[0].tex()} {self.args[1].tex()} \right)"


class SumS(DiracNotation, MultiBindTerm):
    fsymbol_print = "sums"
    fsymbol = "SUMS"

    def __str__(self) -> str:
        vars_names = ", ".join([v.name for v in self.bind_vars])
        return str(HSeqBlock(
            IndexBlock('__\n\\ \n/ \n‾‾', D_index=vars_names), " ", str(self.body)))

    def tex(self) -> str:
        vars_names = ", ".join([v.name for v in self.bind_vars])
        return rf" \left ( \sum_{{{vars_names}}} {self.body.tex()} \right )"
    

class Sum(DiracNotation, MultiBindTerm):
    fsymbol_print = "sum"
    fsymbol = "SUM"

    def __str__(self) -> str:
        vars_names = ", ".join([v.name for v in self.bind_vars])
        return str(HSeqBlock(
            IndexBlock('__\n\\ \n/ \n‾‾', D_index=vars_names), " ", str(self.body)))

    def tex(self) -> str:
        vars_names = ", ".join([v.name for v in self.bind_vars])
        return rf" \left ( \sum_{{{vars_names}}} {self.body.tex()} \right )"
    

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




