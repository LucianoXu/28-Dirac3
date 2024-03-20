
from __future__ import annotations

from diracdec.ast import *

from diracdec.backends.formprint import *

from typing import Type, Tuple

from abc import abstractmethod, ABC


INDENT = "  "

class Ast(ABC):

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        raise NotImplementedError()
    
    def __matmul__(self, other: Ast) -> Ast:
        return Seq((self, other))


#####################################################################
# different program structures
    

class Abort(Ast):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "abort;"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Abort)
    

class Skip(Ast):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "skip;"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Skip)
    

class Init(Ast):
    def __init__(self, qvar : Term):
        self.qvar = qvar
    
    def __str__(self, prefix="") -> str:
        return str(HSeqBlock(str(self.qvar), ":=0", v_align='c'))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Init) and self.qvar == other.qvar

    
class Unitary(Ast):
    def __init__(self, U : Term):
        self.U = U

    def __str__(self) -> str:
        return str(HSeqBlock(str(self.U), ";", v_align='c'))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Unitary) and self.U == other.U
    


# class Assert(Ast):
#     def __init__(self, P : Term):
#         self.P = P

#     def __str__(self) -> str:
#         return str(self.P)
    


class Seq(Ast):
    def __init__(self, S_ls : Tuple[Ast, ...]):
        super().__init__()
        
        self.S_ls = []
        
        # flatten the sequence
        for prog in S_ls:
            if isinstance(prog, Seq):
                self.S_ls = self.S_ls + prog.S_ls
            else:
                self.S_ls.append(prog)

    
    def __str__(self) -> str:
        return str(VSeqBlock(
            *tuple(str(s) for s in self.S_ls),
            h_align='l'))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Seq) and self.S_ls == other.S_ls
    

class If(Ast):
    def __init__(self, M : Term, S1 : Ast, S0 : Ast):
        super().__init__()
        
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
    
    def __eq__(self, other) -> bool:
        return isinstance(other, If) and self.M == other.M and self.S1 == other.S1 and self.S0 == other.S0

class While(Ast):
    def __init__(self, M : Term, S : Ast):
        super().__init__()
        
        self.M = M
        self.S = S

    
    def __str__(self) -> str:
        return str(VSeqBlock(
            HSeqBlock("while ", str(self.M), " do", v_align='c'),
            HSeqBlock(INDENT, str(self.S)),
            "end;",
            h_align='l'))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, While) and self.M == other.M and self.S == other.S