
from __future__ import annotations

from diracdec.ast import *

from diracdec.backends.formprint import *

from typing import Type, Tuple

from abc import abstractmethod, ABC


INDENT = "  "

class QWhileAst(StdTerm):

    def tex(self) -> str:
        raise NotImplementedError()
    
    def __matmul__(self, other: QWhileAst) -> QWhileAst:
        return Seq(self, other)


#####################################################################
# different program structures
    

class Abort(QWhileAst):
    fsymbol_print = 'abort'
    fsymbol = 'abort'

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "abort;"


class Skip(QWhileAst):
    fsymbol_print = 'skip'
    fsymbol = 'skip'

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "skip;"
    


class Init(QWhileAst):
    fsymbol_print = 'init'
    fsymbol = 'init'

    def __init__(self, qvar : Term):
        super().__init__(qvar)
        self.qvar = qvar
    
    def __str__(self, prefix="") -> str:
        return str(HSeqBlock(str(self.qvar), ":=0", v_align='c'))
    

    
class Unitary(QWhileAst):
    fsymbol_print = 'unitary'
    fsymbol = 'unitary'

    def __init__(self, U : Term):
        super().__init__(U)
        self.U = U

    def __str__(self) -> str:
        return str(HSeqBlock(str(self.U), ";", v_align='c'))


class Seq(QWhileAst):
    fsymbol_print = 'seq'
    fsymbol = 'seq'

    def __init__(self, S0 : QWhileAst, S1: QWhileAst):

        # restructure the sequential composition, so that it is always associated to the right
        if isinstance(S0, Seq):
            S0, S1 = S0.S0, Seq(S0.S1, S1)

        super().__init__(S0, S1)
        
        self.S0 = S0
        self.S1 = S1

    
    def __str__(self) -> str:
        return str(VSeqBlock(
            str(self.S0),
            str(self.S1),
            h_align='l'))
    

class If(QWhileAst):
    fsymbol_print = 'if'
    fsymbol = 'if'

    def __init__(self, M : Term, S1 : QWhileAst, S0 : QWhileAst):
        super().__init__(M, S1, S0)
        
        self.M = M
        self.S1 = S1
        self.S0 = S0
    
    def __str__(self) -> str:
        return str(VSeqBlock(
            HSeqBlock("if ", str(self.M), " then ", v_align='c'),
            HSeqBlock(INDENT, str(self.S1)),
            "else",
            HSeqBlock(INDENT, str(self.S0)),
            "end;",
            h_align='l'))
    

class While(QWhileAst):
    fsymbol_print = 'while'
    fsymbol = 'while'

    def __init__(self, M : Term, S : QWhileAst):
        super().__init__(M, S)
        
        self.M = M
        self.S = S

    
    def __str__(self) -> str:
        return str(VSeqBlock(
            HSeqBlock("while ", str(self.M), " do", v_align='c'),
            HSeqBlock(INDENT, str(self.S)),
            "end;",
            h_align='l'))