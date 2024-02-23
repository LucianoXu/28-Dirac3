
from __future__ import annotations

from ..trs import TRSTerm, TRSVar, StdTerm, TRS_AC, TRSCommBinary, TRSInfixBinary, Subst



class DiracSyntax:
    ...

############################################
# DiracBase

class DiracBase(DiracSyntax):
    ...
    
    
class BasePair(DiracBase, StdTerm):
    fsymbol_print = "pair"
    fsymbol = "PAIR"
    
    def __init__(self, left: TRSTerm, right: TRSTerm):
        super().__init__(left, right)
    
    def __str__(self) -> str:
        return f"({self.args[0]}, {self.args[1]})"
    
    def tex(self) -> str:
        return f"( {self.args[0].tex()} , {self.args[1].tex()} )"
    
    
    
class BaseFst(DiracBase, StdTerm):
    fsymbol_print = "fst"
    fsymbol = "FST"

    def __init__(self, p: TRSTerm):
        super().__init__(p)

    def tex(self) -> str:
        return rf" \mathrm{{fst}} {self.args[0].tex()}"
    
class BaseSnd(DiracBase, StdTerm):
    fsymbol_print = "snd"
    fsymbol = "SND"

    def __init__(self, p: TRSTerm):
        super().__init__(p)

    def tex(self) -> str:
        return rf" \mathrm{{snd}} {self.args[0].tex()}"
    

############################################
# DiracScalar

class DiracScalar(DiracSyntax):
    ...


class ScalarDelta(DiracScalar, TRSCommBinary):
    fsymbol_print = "δ"
    fsymbol = "DELTA"

    def __init__(self, b1 : TRSTerm, b2 : TRSTerm):
        TRSCommBinary.__init__(self, b1, b2)

    def tex(self) -> str:
        return rf" \delta_{{{self.args[0].tex()}, {self.args[1].tex()}}}"


class ScalarAdd(DiracScalar, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDS'

    def __init__(self, *tup : TRSTerm):
        TRS_AC.__init__(self, *tup)

    
class ScalarMlt(DiracScalar, TRS_AC):
    fsymbol_print = '×'
    fsymbol = 'MLTS'

    def __init__(self, *tup : TRSTerm):
        TRS_AC.__init__(self, *tup)

    def tex(self) -> str:
        return "( " + " \times ".join([s.tex() for s in self.args]) + " )"

class ScalarConj(DiracScalar, StdTerm):
    fsymbol_print = "CONJS"
    fsymbol = "CONJS"

    def __init__(self, s: TRSTerm):
        super().__init__(s)

    def __str__(self) -> str:
        return f"({self.args[0]}^*)"
    
    def tex(self) -> str:
        return f" {self.args[0].tex()}^*"
    
    
class ScalarDot(DiracScalar, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "DOT"

    def __init__(self, B: TRSTerm, K: TRSTerm):
        super().__init__(B, K)

    def tex(self) -> str:
        # special printing for <b|k>
        if isinstance(self.args[0], BraBase) and isinstance(self.args[1], KetBase):
            return rf" \langle {self.args[0].args[0].tex()} | {self.args[1].args[0].tex()} \rangle"
        
        return rf" ({self.args[0].tex()} \cdot {self.args[1].tex()})"


############################################
# DiracKet
    
class DiracKet(DiracSyntax):
    ...

class KetZero(DiracKet, StdTerm):
    fsymbol_print = "0K"
    fsymbol = "0K"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "0K"
    
    def __repr__(self) -> str:
        return "0K"
    
    def tex(self) -> str:
        return r" \mathbf{0}_\mathcal{K}"
    
    
class KetBase(DiracKet, StdTerm):
    fsymbol_print = "ket"
    fsymbol = "KET"

    def __init__(self, b : TRSTerm):
        super().__init__(b)
    
    def __str__(self) -> str:
        return f"|{self.args[0]}>"
    
    def tex(self) -> str:
        return rf" |{self.args[0].tex()} \rangle"
    
    
class KetAdj(DiracKet, StdTerm):
    fsymbol_print = "ADJK"
    fsymbol = "ADJK"

    def __init__(self, B: TRSTerm):
        super().__init__(B)

    def __str__(self) -> str:
        return f"({self.args[0]}†)"
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^\dagger"
    

class KetScal(DiracKet, TRSInfixBinary):
    fsymbol_print = "."
    fsymbol = "SCRK"

    def __init__(self, S: TRSTerm, K: TRSTerm):
        TRSInfixBinary.__init__(self, S, K)

    def tex(self) -> str:
        return rf" {self.args[0].tex()} {self.args[1].tex()}"

    
class KetAdd(DiracKet, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDK'

    def __init__(self, *tup : TRSTerm):
        TRS_AC.__init__(self, *tup)
    
class KetApply(DiracKet, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTK"

    def __init__(self, O: TRSTerm, K: TRSTerm) :
        TRSInfixBinary.__init__(self, O, K)

    def tex(self) -> str:
        if isinstance(self.args[1], KetBase):
            return rf" {self.args[0].tex()} {self.args[1].tex()}"
        else:
            return rf" {self.args[0].tex()} \cdot {self.args[1].tex()}"


class KetTensor(DiracKet, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRK"

    def __init__(self, K1: TRSTerm, K2: TRSTerm) :
        TRSInfixBinary.__init__(self, K1, K2)

    def tex(self) -> str:
        return rf" \left ({self.args[0].tex()} \otimes {self.args[1].tex()} \right)"
    

############################################
# DiracBra
        
class DiracBra(DiracSyntax):
    ...

class BraZero(DiracBra, StdTerm):
    fsymbol_print = "0B"
    fsymbol = "0B"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "0B"
    
    def __repr__(self) -> str:
        return "0B"
    
    def tex(self) -> str:
        return r" \mathbf{0}_\mathcal{B}"
    
class BraBase(DiracBra, StdTerm):
    fsymbol_print = "bra"
    fsymbol = "BRA"

    def __init__(self, b : TRSTerm):
        super().__init__(b)
    
    def __str__(self) -> str:
        return f"<{self.args[0]}|"
    
    def tex(self) -> str:
        return rf" \langle {self.args[0].tex()} |"
    


class BraAdj(DiracBra, StdTerm):
    fsymbol_print = "ADJB"
    fsymbol = "ADJB"

    def __init__(self, K: TRSTerm):
        super().__init__(K)

    def __str__(self) -> str:
        return f"({self.args[0]}†)"
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^\dagger"
    

class BraScal(DiracBra, TRSInfixBinary):
    fsymbol_print = "."
    fsymbol = "SCRB"

    def __init__(self, S: TRSTerm, B: TRSTerm):
        TRSInfixBinary.__init__(self, S, B)

    def tex(self) -> str:
        return rf" {self.args[0].tex()} {self.args[1].tex()}"

    
class BraAdd(DiracBra, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDB'

    def __init__(self, *tup : TRSTerm):
        TRS_AC.__init__(self, *tup)
    

class BraApply(DiracBra, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTB"

    def __init__(self, B: TRSTerm, O: TRSTerm) :
        TRSInfixBinary.__init__(self, B, O)

    def tex(self) -> str:
        if isinstance(self.args[0], BraBase):
            return rf" {self.args[0].tex()} {self.args[1].tex()}"
        else:
            return rf" {self.args[0].tex()} \cdot {self.args[1].tex()}"

    

class BraTensor(DiracBra, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRB"

    def __init__(self, B1: TRSTerm, B2: TRSTerm) :
        TRSInfixBinary.__init__(self, B1, B2)

    def tex(self) -> str:
        return rf" \left ( {self.args[0].tex()} \otimes {self.args[1].tex()} \right )"

############################################
# DiracOp
    
class DiracOp(DiracSyntax):
    ...


class OpZero(DiracOp, StdTerm):
    fsymbol_print = "0O"
    fsymbol = "0O"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "0O"
    
    def __repr__(self) -> str:
        return "0O"
    
    def tex(self) -> str:
        return r" \mathbf{0}_\mathcal{O}"

class OpOne(DiracOp, StdTerm):
    fsymbol_print = "1O"
    fsymbol = "1O"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "1O"
    
    def __repr__(self) -> str:
        return "1O"
    
    def tex(self) -> str:
        return r" \mathbf{1}_\mathcal{O}"
    
    
class OpOuter(DiracOp, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "OUTER"

    def __init__(self, K: TRSTerm, B: TRSTerm):
        TRSInfixBinary.__init__(self, K, B)

    def tex(self) -> str:
        if isinstance(self.args[0], KetBase) and isinstance(self.args[1], BraBase):
            return rf" {self.args[0].tex()} {self.args[1].tex()}"
        
        return rf" {self.args[0].tex()} \otimes {self.args[1].tex()}"
    
class OpAdj(DiracOp, StdTerm):
    fsymbol_print = "ADJO"
    fsymbol = "ADJO"

    def __init__(self, O: TRSTerm) :
        super().__init__(O)

    def __str__(self) -> str:
        return f"({self.args[0]}†)"
    
    def __repr__(self) -> str:
        return f"ADJO({repr(self.args[0])})"
    
    def tex(self) -> str:
        return rf" {self.args[0].tex()}^\dagger"
    
    
class OpScal(DiracOp, TRSInfixBinary):
    fsymbol_print = "."
    fsymbol = "SCRO"

    def __init__(self, S: TRSTerm, O: TRSTerm) :
        TRSInfixBinary.__init__(self, S, O)

    def tex(self) -> str:
        return rf" {self.args[0].tex()} {self.args[1].tex()}"

    
class OpAdd(DiracOp, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDO'

    def __init__(self, *tup : TRSTerm):
        TRS_AC.__init__(self, *tup)

    
class OpApply(DiracOp, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTO"

    def __init__(self, O1: TRSTerm, O2: TRSTerm) :
        TRSInfixBinary.__init__(self, O1, O2)

    def tex(self) -> str:
        return rf" {self.args[0].tex()} \cdot {self.args[1].tex()}"


class OpTensor(DiracOp, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRO"

    def __init__(self, O1: TRSTerm, O2: TRSTerm) :
        TRSInfixBinary.__init__(self, O1, O2)

    def tex(self) -> str:
        return rf" \left ( {self.args[0].tex()} \otimes {self.args[1].tex()} \right ) "