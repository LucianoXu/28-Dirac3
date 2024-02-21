
from __future__ import annotations

from ..atomic_base import AtomicBase
from ..complex_scalar import ComplexScalar

from ..trs import TRSTerm, TRSVar, TRS_AC, TRSCommBinary, TRSInfixBinary, Subst



class DiracSyntax(TRSTerm):
    def substitute(self, sigma: Subst) -> TRSTerm:
        return super().substitute(sigma)

############################################
# DiracBase

class DiracBase(DiracSyntax):
    ...
    
    
class BaseAtom(DiracBase):
    fsymbol_print = "BATOM"
    fsymbol = "BATOM"

    def __init__(self, b : AtomicBase | TRSVar):
        '''
        b is the atomic base
        '''
        super().__init__(b)
    
    def __str__(self) -> str:
        return f"'{str(self.args[0])}'"
    
    def __repr__(self) -> str:
        return f"'{repr(self.args[0])}'"
    
    
class BasePair(DiracBase):
    fsymbol_print = "pair"
    fsymbol = "PAIR"
    
    def __init__(self, left: DiracBase | TRSVar, right: DiracBase | TRSVar):
        super().__init__(left, right)
    
    def __str__(self) -> str:
        return f"({self.args[0]}, {self.args[1]})"
    
    
    
class BaseFst(DiracBase):
    fsymbol_print = "fst"
    fsymbol = "FST"

    def __init__(self, p: BasePair | TRSVar):
        super().__init__(p)
    
class BaseSnd(DiracBase):
    fsymbol_print = "snd"
    fsymbol = "SND"

    def __init__(self, p: BasePair | TRSVar):
        super().__init__(p)
    

############################################
# DiracScalar

class DiracScalar(DiracSyntax):
    ...


class ScalarC(DiracScalar):
    fsymbol_print = "ScalarC"
    fsymbol = "ScalarC"

    def __init__(self, c : ComplexScalar|TRSVar):
        super().__init__(c)

    def __str__(self) -> str:
        return f'"{self.args[0]}"'
    
    def __repr__(self) -> str:
        return f'"{repr(self.args[0])}"'


class ScalarDelta(DiracScalar, TRSCommBinary):
    fsymbol_print = "δ"
    fsymbol = "DELTA"

    def __init__(self, b1 : DiracBase | TRSVar, b2 : DiracBase | TRSVar):
        TRSCommBinary.__init__(self, b1, b2)


class ScalarAdd(DiracScalar, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDS'

    def __init__(self, *tup : DiracScalar | TRSVar):
        TRS_AC.__init__(self, *tup)

    
class ScalarMlt(DiracScalar, TRS_AC):
    fsymbol_print = '×'
    fsymbol = 'MLTS'

    def __init__(self, *tup : DiracScalar | TRSVar):
        TRS_AC.__init__(self, *tup)


class ScalarConj(DiracScalar):
    fsymbol_print = "CONJS"
    fsymbol = "CONJS"

    def __init__(self, s : DiracScalar | TRSVar):
        super().__init__(s)

    def __str__(self) -> str:
        return f"({self.args[0]}^*)"
    
    
class ScalarDot(DiracScalar, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "DOT"

    def __init__(self, B: DiracBra|TRSVar, K: DiracKet|TRSVar):
        super().__init__(B, K)


############################################
# DiracKet
    
class DiracKet(DiracSyntax):
    ...

class KetZero(DiracKet):
    fsymbol_print = "0K"
    fsymbol = "ZEROK"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "0K"
    
    def __repr__(self) -> str:
        return "ZEROK"
    
    
class KetBase(DiracKet):
    fsymbol_print = "ket"
    fsymbol = "KET"

    def __init__(self, b : DiracBase | TRSVar):
        super().__init__(b)
    
    def __str__(self) -> str:
        return f"|{self.args[0]}>"
    
    
class KetAdj(DiracKet):
    fsymbol_print = "ADJK"
    fsymbol = "ADJK"

    def __init__(self, B: DiracBra|TRSVar):
        super().__init__(B)

    def __str__(self) -> str:
        return f"({self.args[0]}†)"
    

class KetScal(DiracKet, TRSInfixBinary):
    fsymbol_print = "."
    fsymbol = "SCRK"

    def __init__(self, S: DiracScalar|TRSVar, K: DiracKet|TRSVar):
        TRSInfixBinary.__init__(self, S, K)

    
class KetAdd(DiracKet, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDK'

    def __init__(self, *tup : DiracKet|TRSVar):
        TRS_AC.__init__(self, *tup)
    
class KetApply(DiracKet, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTK"

    def __init__(self, O: DiracOp|TRSVar, K: DiracKet|TRSVar) :
        TRSInfixBinary.__init__(self, O, K)


class KetTensor(DiracKet, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRK"

    def __init__(self, K1: DiracKet|TRSVar, K2: DiracKet|TRSVar) :
        TRSInfixBinary.__init__(self, K1, K2)
    

############################################
# DiracBra
        
class DiracBra(DiracSyntax):
    ...

class BraZero(DiracBra):
    fsymbol_print = "0B"
    fsymbol = "ZEROB"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "0B"
    
    def __repr__(self) -> str:
        return "ZEROB"
    
class BraBase(DiracBra):
    fsymbol_print = "bra"
    fsymbol = "BRA"

    def __init__(self, b : DiracBase | TRSVar):
        super().__init__(b)
    
    def __str__(self) -> str:
        return f"<{self.args[0]}|"
    


class BraAdj(DiracBra):
    fsymbol_print = "ADJB"
    fsymbol = "ADJB"

    def __init__(self, K: DiracBra|TRSVar):
        super().__init__(K)

    def __str__(self) -> str:
        return f"({self.args[0]}†)"
    

class BraScal(DiracBra, TRSInfixBinary):
    fsymbol_print = "."
    fsymbol = "SCRB"

    def __init__(self, S: DiracScalar|TRSVar, B: DiracBra|TRSVar):
        TRSInfixBinary.__init__(self, S, B)

    
class BraAdd(DiracBra, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDB'

    def __init__(self, *tup : DiracBra|TRSVar):
        TRS_AC.__init__(self, *tup)
    

class BraApply(DiracBra, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTB"

    def __init__(self, B: DiracBra|TRSVar, O: DiracOp|TRSVar) :
        TRSInfixBinary.__init__(self, B, O)

    

class BraTensor(DiracBra, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRB"

    def __init__(self, B1: DiracBra|TRSVar, B2: DiracBra|TRSVar) :
        TRSInfixBinary.__init__(self, B1, B2)

############################################
# DiracOp
    
class DiracOp(DiracSyntax):
    ...


class OpZero(DiracOp):
    fsymbol_print = "0O"
    fsymbol = "ZEROO"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "0O"
    
    def __repr__(self) -> str:
        return "ZEROO"
    

class OpOne(DiracOp):
    fsymbol_print = "1O"
    fsymbol = "ONEO"

    def __init__(self) :
        super().__init__()

    def __str__(self) -> str:
        return "1O"
    
    def __repr__(self) -> str:
        return "ONEO"
    
    
class OpOuter(DiracOp, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "OUTER"

    def __init__(self, K: DiracKet|TRSVar, B: DiracBra|TRSVar):
        TRSInfixBinary.__init__(self, K, B)
    
class OpAdj(DiracOp):
    fsymbol_print = "ADJO"
    fsymbol = "ADJO"

    def __init__(self, O: DiracOp|TRSVar) :
        super().__init__(O)

    def __str__(self) -> str:
        return f"({self.args[0]}†)"
    
    def __repr__(self) -> str:
        return f"ADJO({repr(self.args[0])})"
    
    
class OpScal(DiracOp, TRSInfixBinary):
    fsymbol_print = "."
    fsymbol = "SCRO"

    def __init__(self, S: DiracScalar|TRSVar, O: DiracOp|TRSVar) :
        TRSInfixBinary.__init__(self, S, O)

    
class OpAdd(DiracOp, TRS_AC):
    fsymbol_print = '+'
    fsymbol = 'ADDO'

    def __init__(self, *tup : DiracOp|TRSVar):
        TRS_AC.__init__(self, *tup)

    
class OpApply(DiracOp, TRSInfixBinary):
    fsymbol_print = "·"
    fsymbol = "MLTO"

    def __init__(self, O1: DiracOp|TRSVar, O2: DiracOp|TRSVar) :
        TRSInfixBinary.__init__(self, O1, O2)


class OpTensor(DiracOp, TRSInfixBinary):
    fsymbol_print = "⊗"
    fsymbol = "TSRO"

    def __init__(self, O1: DiracOp|TRSVar, O2: DiracOp|TRSVar) :
        TRSInfixBinary.__init__(self, O1, O2)