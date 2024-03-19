
from __future__ import annotations

from ..trs import Term, Var, StdTerm, AC, CommBinary, InfixBinary, Subst

from ...backends.formprint import *

class DiracSyntax:
    ...

############################################
# DiracBase

class DiracBase(DiracSyntax):
    ...
    
    
class BasePair(DiracBase, StdTerm):
    fsymbol_print = "pair"
    fsymbol = "PAIR"
    
    def __init__(self, left: Term, right: Term):
        super().__init__(left, right)
    
    def __str__(self) -> str:
        return str(ParenBlock(HSeqBlock(
            str(self.args[0]), ', ', str(self.args[1]),
            v_align='b')))

    def tex(self) -> str:
        return f"( {self.args[0].tex()} , {self.args[1].tex()} )"
    
    
    
class BaseFst(DiracBase, StdTerm):
    fsymbol_print = "fst"
    fsymbol = "FST"

    def __init__(self, p: Term):
        super().__init__(p)

    def tex(self) -> str:
        return rf" \mathrm{{fst}} {self.args[0].tex()}"
    
class BaseSnd(DiracBase, StdTerm):
    fsymbol_print = "snd"
    fsymbol = "SND"

    def __init__(self, p: Term):
        super().__init__(p)

    def tex(self) -> str:
        return rf" \mathrm{{snd}} {self.args[0].tex()}"
    

############################################
# DiracScalar

class DiracScalar(DiracSyntax):
    ...


class ScalarDelta(DiracScalar, CommBinary):
    fsymbol_print = "δ"
    fsymbol = "DELTA"

    def __init__(self, b1 : Term, b2 : Term):
        CommBinary.__init__(self, b1, b2)

    def tex(self) -> str:
        return rf" \delta_{{{self.args[0].tex()}, {self.args[1].tex()}}}"


class ScalarAdd(DiracScalar, AC):
    fsymbol_print = '+'
    fsymbol = 'ADDS'

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)

    
class ScalarMlt(DiracScalar, AC):
    fsymbol_print = '×'
    fsymbol = 'MLTS'

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)

    def tex(self) -> str:
        return "( " + " \\times ".join([s.tex() for s in self.args]) + " )"

class ScalarConj(DiracScalar, StdTerm):
    fsymbol_print = "CONJS"
    fsymbol = "CONJS"

    def __init__(self, s: Term):
        super().__init__(s)

    def __str__(self) -> str:
        return str(IndexBlock(str(self.args[0]), UR_index='*'))
    
    def tex(self) -> str:
        return f" {self.args[0].tex()}^*"
    
    
class ScalarDot(DiracScalar, InfixBinary):
    fsymbol_print = "·"
    fsymbol = "DOT"

    def __init__(self, B: Term, K: Term):
        super().__init__(B, K)

    def tex(self) -> str:
        # special printing for <b|k>
        if isinstance(self.args[0], BraBase) and isinstance(self.args[1], KetBase):
            return rf" \langle {self.args[0].args[0].tex()} | {self.args[1].args[0].tex()} \rangle"
        
        return rf" ({self.args[0].tex()} \cdot {self.args[1].tex()})"


class DiracNotation(DiracSyntax):
    ...

############################################
# Unified Symbol
    
class Zero(DiracNotation, StdTerm):
    fsymbol_print = "𝟎"
    fsymbol = "0X"

    def __str__(self) -> str:
        return "𝟎"
    
    def __repr__(self) -> str:
        return "0X"
    
    def tex(self) -> str:
        return r" \mathbf{0}"
        

class Adj(DiracNotation, StdTerm):
    fsymbol_print = "ADJ"
    fsymbol = "ADJ"

    def __init__(self, X: Term):
        super().__init__(X)

    def __str__(self) -> str:
        return str(IndexBlock(str(self.args[0]), UR_index="†"))
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^\dagger"
    

class Scal(DiracNotation, InfixBinary):
    fsymbol_print = "."
    fsymbol = "SCR"

    def __init__(self, S: Term, X: Term):
        InfixBinary.__init__(self, S, X)

    def tex(self) -> str:
        return rf" {self.args[0].tex()} {self.args[1].tex()}"

    
class Add(DiracNotation, AC):
    fsymbol_print = '+'
    fsymbol = 'ADD'

    def __init__(self, *tup : Term):
        AC.__init__(self, *tup)
    
        
############################################
# DiracKet
        
class KetBase(DiracNotation, StdTerm):
    fsymbol_print = "ket"
    fsymbol = "KET"

    def __init__(self, b : Term):
        super().__init__(b)
    
    def __str__(self) -> str:
        return str(HSeqBlock("|", str(self.args[0]), ">"))
    
    def tex(self) -> str:
        return rf" |{self.args[0].tex()} \rangle"
    
    
class KetApply(DiracNotation, InfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTK"

    def __init__(self, O: Term, K: Term) :
        InfixBinary.__init__(self, O, K)

    def tex(self) -> str:
        if isinstance(self.args[1], KetBase):
            return rf" {self.args[0].tex()} {self.args[1].tex()}"
        else:
            return rf" {self.args[0].tex()} \cdot {self.args[1].tex()}"


class KetTensor(DiracNotation, InfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRK"

    def __init__(self, K1: Term, K2: Term) :
        InfixBinary.__init__(self, K1, K2)

    def tex(self) -> str:
        return rf" \left ({self.args[0].tex()} \otimes {self.args[1].tex()} \right)"
    

############################################
# DiracBra
        
class BraBase(DiracNotation, StdTerm):
    fsymbol_print = "bra"
    fsymbol = "BRA"

    def __init__(self, b : Term):
        super().__init__(b)
    
    def __str__(self) -> str:
        return str(HSeqBlock("<", str(self.args[0]), "|"))
    
    def tex(self) -> str:
        return rf" \langle {self.args[0].tex()} |"
    

class BraApply(DiracNotation, InfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTB"

    def __init__(self, B: Term, O: Term) :
        InfixBinary.__init__(self, B, O)

    def tex(self) -> str:
        if isinstance(self.args[0], BraBase):
            return rf" {self.args[0].tex()} {self.args[1].tex()}"
        else:
            return rf" {self.args[0].tex()} \cdot {self.args[1].tex()}"

    
class BraTensor(DiracNotation, InfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRB"

    def __init__(self, B1: Term, B2: Term) :
        InfixBinary.__init__(self, B1, B2)

    def tex(self) -> str:
        return rf" \left ( {self.args[0].tex()} \otimes {self.args[1].tex()} \right )"


############################################
# DiracOp
    
class OpOne(DiracNotation, StdTerm):
    fsymbol_print = "𝟏"
    fsymbol = "1O"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "𝟏"
    
    def __repr__(self) -> str:
        return "1O"
    
    def tex(self) -> str:
        return r" \mathbf{1}"
    
    
class OpOuter(DiracNotation, InfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "OUTER"

    def __init__(self, K: Term, B: Term):
        InfixBinary.__init__(self, K, B)

    def tex(self) -> str:
        if isinstance(self.args[0], KetBase) and isinstance(self.args[1], BraBase):
            return rf" {self.args[0].tex()} {self.args[1].tex()}"
        
        return rf" {self.args[0].tex()} \otimes {self.args[1].tex()}"

    
class OpApply(DiracNotation, InfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTO"

    def __init__(self, O1: Term, O2: Term) :
        InfixBinary.__init__(self, O1, O2)

    def tex(self) -> str:
        return rf" {self.args[0].tex()} \cdot {self.args[1].tex()}"


class OpTensor(DiracNotation, InfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRO"

    def __init__(self, O1: Term, O2: Term) :
        InfixBinary.__init__(self, O1, O2)

    def tex(self) -> str:
        return rf" \left ( {self.args[0].tex()} \otimes {self.args[1].tex()} \right ) "