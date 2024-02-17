
from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Tuple, List, Type

from .atomic_base import AtomicBase
from .complex_scalar import ComplexScalar

from .trs import TRSTerm, TRSVar


# note: repr method outputs the precise expression, and str method outputs the pretty printing

################################################################
# techniques for AC-symbols


class AC_symbol:
    PRINTING_INFIX : str
    EXPR_INFIX : str

    def __init__(self, tup: Tuple):
        '''
        The method of flatten the tuple of arguments for the ac_symbol.
        Assume that the items in tup are already flattened.
        '''
        if len(tup) < 2:
            raise ValueError("The tuple lengh should be at least 2.")

        new_ls = []
        for item in tup:
            if isinstance(item, type(self)):
                new_ls.extend(item.tup)
            else:
                new_ls.append(item)

        self.tup = tuple(sorted(new_ls, key=lambda x: hash(x)))

    def __str__(self) -> str:
        return f"({f' {self.PRINTING_INFIX} '.join(map(str, self.tup))})"
    
    def __repr__(self) -> str:
        return f"({f' {self.EXPR_INFIX} '.join(map(str, map(repr, self.tup)))})"

    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(tuple([hash(item) for item in self.tup]))


class DiracSyntax(TRSTerm):
    def __hash__(self) -> int:
        return super().__hash__()

############################################
# DiracBase

class DiracBase(DiracSyntax):
    def __hash__(self) -> int:
        return super().__hash__()
    
    
class BaseAtom(DiracBase):

    def __init__(self, b : AtomicBase | TRSVar):
        '''
        b is the atomic base
        '''
        self.b = b
    
    def __str__(self) -> str:
        return f"'{str(self.b)}'"
    
    def __repr__(self) -> str:
        return f"'{repr(self.b)}'"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BaseAtom) and self.b == other.b
    
    def __hash__(self) -> int:
        return super().__hash__()

    
    def args_hash(self) -> int:
        return hash(self.b)
    
    
class BasePair(DiracBase):
    
    def __init__(self, left: DiracBase | TRSVar, right: DiracBase | TRSVar):
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        return f"({self.left}, {self.right})"
    
    def __repr__(self) -> str:
        return f"PAIR({repr(self.left)}, {repr(self.right)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BasePair) and self.left == other.left and self.right == other.right
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash((self.left, self.right))
    
class BaseFst(DiracBase):
    def __init__(self, p: BasePair | TRSVar):
        self.p = p

    def __str__(self) -> str:
        return f"FST({self.p})"
    
    def __repr__(self) -> str:
        return f"FST({repr(self.p)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BaseFst) and self.p == other.p
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.p)
    
class BaseSnd(DiracBase):
    def __init__(self, p: BasePair | TRSVar):
        self.p = p

    def __str__(self) -> str:
        return f"SND({self.p})"
    
    def __repr__(self) -> str:
        return f"SND({repr(self.p)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BaseSnd) and self.p == other.p
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.p)
    

############################################
# DiracScalar

class DiracScalar(DiracSyntax):
    def __hash__(self) -> int:
        return super().__hash__()


class ScalarC(DiracScalar):
    def __init__(self, c : ComplexScalar):
        self.c = c

    def __str__(self) -> str:
        return f'"{self.c}"'
    
    def __repr__(self) -> str:
        return f'"{repr(self.c)}"'
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarC) and self.c == other.c
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.c)

class ScalarDelta(DiracScalar):
    def __init__(self, b1 : AtomicBase | TRSVar, b2 : AtomicBase | TRSVar):
        self.b1 = b1
        self.b2 = b2

    def __str__(self) -> str:
        return f"δ({self.b1}, {self.b2})"
    
    def __repr__(self) -> str:
        return f"DELTA({repr(self.b1)}, {repr(self.b2)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarDelta) and self.b1 == other.b1 and self.b2 == other.b2
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash((self.b1, self.b2))


class ScalarAdd(DiracScalar, AC_symbol):
    PRINTING_INFIX = '+'
    EXPR_INFIX = 'ADDS'

    def __init__(self, tup : Tuple[DiracScalar | TRSVar, ...]):
        AC_symbol.__init__(self, tup)

    def __str__(self) -> str:
        return AC_symbol.__str__(self)
    
    def __repr__(self) -> str:
        return AC_symbol.__repr__(self)
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarAdd) and self.tup == other.tup
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return AC_symbol.args_hash(self)
    
class ScalarMlt(DiracScalar, AC_symbol):
    PRINTING_INFIX = '×'
    EXPR_INFIX = 'MLTS'

    def __init__(self, tup : Tuple[DiracScalar | TRSVar, ...]):
        AC_symbol.__init__(self, tup)

    def __str__(self) -> str:
        return AC_symbol.__str__(self)
    
    def __repr__(self) -> str:
        return AC_symbol.__repr__(self)
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarMlt) and self.tup == other.tup
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return AC_symbol.args_hash(self)
    
class ScalarConj(DiracScalar):
    def __init__(self, s : DiracScalar | TRSVar):
        self.s = s

    def __str__(self) -> str:
        return f"({self.s})^*"
    
    def __repr__(self) -> str:
        return f"CONJS({repr(self.s)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarConj) and self.s == other.s
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.s)
    
class ScalarDot(DiracScalar):
    def __init__(self, B: DiracBra|TRSVar, K: DiracKet|TRSVar):
        self.B = B
        self.K = K

    def __str__(self) -> str:
        return f"({self.B} · {self.K})"
    
    def __repr__(self) -> str:
        return f"({repr(self.B)} DOT {repr(self.K)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarDot) and self.B == other.B and self.K == other.K
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.B, self.K))

############################################
# DiracKet
    
class DiracKet(DiracSyntax):
    def __hash__(self) -> int:
        return super().__hash__()
    

class KetZero(DiracKet):
    def __init__(self) :
        pass

    def __str__(self) -> str:
        return "0K"
    
    def __repr__(self) -> str:
        return "ZEROK"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, KetZero)
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(())
    
    
class KetBase(DiracKet):
    def __init__(self, b : DiracBase | TRSVar):
        self.b = b
    
    def __str__(self) -> str:
        return f"|{self.b}>"
    
    def __repr__(self) -> str:
        return f"KET({repr(self.b)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, KetBase) and self.b == other.b
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.b)
    
class KetAdj(DiracKet):
    def __init__(self, B: DiracBra|TRSVar) :
        self.B = B

    def __str__(self) -> str:
        return f"({self.B})†"
    
    def __repr__(self) -> str:
        return f"ADJK({repr(self.B)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, KetAdj) and self.B == other.B
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(self.B)
    

class KetScal(DiracKet):
    def __init__(self, S: DiracScalar|TRSVar, K: DiracKet|TRSVar) :
        self.S = S
        self.K = K

    def __str__(self) -> str:
        return f"({self.S}.{self.K})"
    
    def __repr__(self) -> str:
        return f"({repr(self.S)} SCRK {repr(self.K)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, KetScal) and self.S == other.S and self.K == other.K
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.S, self.K))
    
class KetAdd(DiracKet, AC_symbol):
    PRINTING_INFIX = '+'
    EXPR_INFIX = 'ADDK'

    def __init__(self, tup : Tuple[DiracKet|TRSVar, ...]):
        AC_symbol.__init__(self, tup)

    def __str__(self) -> str:
        return AC_symbol.__str__(self)
    
    def __repr__(self) -> str:
        return AC_symbol.__repr__(self)
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, KetAdd) and self.tup == other.tup
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return AC_symbol.args_hash(self)
    
class KetApply(DiracKet):
    def __init__(self, O: DiracOp|TRSVar, K: DiracKet|TRSVar) :
        self.O = O
        self.K = K

    def __str__(self) -> str:
        return f"({self.O} · {self.K})"
    
    def __repr__(self) -> str:
        return f"({repr(self.O)} MLTK {repr(self.K)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, KetApply) and self.O == other.O and self.K == other.K
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.O, self.K))
    

class KetTensor(DiracKet):
    def __init__(self, K1: DiracKet|TRSVar, K2: DiracKet|TRSVar) :
        self.K1 = K1
        self.K2 = K2

    def __str__(self) -> str:
        return f"({self.K1} ⊗ {self.K2})"
    
    def __repr__(self) -> str:
        return f"({repr(self.K1)} TSRK {repr(self.K2)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, KetTensor) and self.K1 == other.K1 and self.K2 == other.K2
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.K1, self.K2))
    

    

############################################
# DiracBra
    
class DiracBra(DiracSyntax):
    def __hash__(self) -> int:
        return super().__hash__()

class BraZero(DiracBra):
    def __init__(self) :
        pass

    def __str__(self) -> str:
        return "0B"
    
    def __repr__(self) -> str:
        return "ZEROB"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BraZero)
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(())
    
class BraBase(DiracBra):
    def __init__(self, b : DiracBase|TRSVar) :
        self.b = b

    def __str__(self) -> str:
        return f"<{self.b}|"
    
    def __repr__(self) -> str:
        return f"BRA({repr(self.b)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BraBase) and self.b == other.b
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(self.b)
    
class BraAdj(DiracBra):
    def __init__(self, K: DiracKet|TRSVar) :
        self.K = K

    def __str__(self) -> str:
        return f"({self.K})†"
    
    def __repr__(self) -> str:
        return f"ADJB({repr(self.K)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BraAdj) and self.K == other.K
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(self.K)
    
class BraScal(DiracBra):
    def __init__(self, S: DiracScalar|TRSVar, B: DiracBra|TRSVar) :
        self.S = S
        self.B = B

    def __str__(self) -> str:
        return f"({self.S}.{self.B})"
    
    def __repr__(self) -> str:
        return f"({repr(self.S)} SCRB {repr(self.B)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BraScal) and self.S == other.S and self.B == other.B
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.S, self.B))
    
class BraAdd(DiracBra, AC_symbol):
    PRINTING_INFIX = '+'
    EXPR_INFIX = 'ADDB'
    
    def __init__(self, tup : Tuple[DiracBra|TRSVar, ...]):
        AC_symbol.__init__(self, tup)

    def __str__(self) -> str:
        return AC_symbol.__str__(self)

    def __repr__(self) -> str:
        return AC_symbol.__repr__(self)
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BraAdd) and self.tup == other.tup
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return AC_symbol.args_hash(self)
    

class BraApply(DiracBra):
    def __init__(self, B: DiracBra|TRSVar, O: DiracOp|TRSVar) :
        self.B = B
        self.O = O

    def __str__(self) -> str:
        return f"({self.B} · {self.O})"
    
    def __repr__(self) -> str:
        return f"({repr(self.B)} MLTB {repr(self.O)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BraApply) and self.B == other.B and self.O == other.O
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.B, self.O))
    
class BraTensor(DiracBra):
    def __init__(self, B1: DiracBra|TRSVar, B2: DiracBra|TRSVar) :
        self.B1 = B1
        self.B2 = B2

    def __str__(self) -> str:
        return f"({self.B1} ⊗ {self.B2})"
    
    def __repr__(self) -> str:
        return f"({repr(self.B1)} TSRB {repr(self.B2)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, BraTensor) and self.B1 == other.B1 and self.B2 == other.B2
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.B1, self.B2))

############################################
# DiracOp
    
class DiracOp(DiracSyntax):
    def __hash__(self) -> int:
        return super().__hash__()

class OpZero(DiracOp):
    def __init__(self) :
        pass

    def __str__(self) -> str:
        return "0O"
    
    def __repr__(self) -> str:
        return "ZEROO"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpZero)
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(())
    

class OpOne(DiracOp):
    def __init__(self) :
        pass

    def __str__(self) -> str:
        return "1O"
    
    def __repr__(self) -> str:
        return "ONEO"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpOne)
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(())
    
class OpOuter(DiracOp):
    def __init__(self, K: DiracKet|TRSVar, B: DiracBra|TRSVar) :
        self.K = K
        self.B = B

    def __str__(self) -> str:
        return f"({self.K} ⊗ {self.B})"
    
    def __repr__(self) -> str:
        return f"({repr(self.K)} OUTER {repr(self.B)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpOuter) and self.K == other.K and self.B == other.B
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.K, self.B))
    
class OpAdj(DiracOp):
    def __init__(self, O: DiracOp|TRSVar) :
        self.O = O

    def __str__(self) -> str:
        return f"({self.O})†"
    
    def __repr__(self) -> str:
        return f"ADJO({repr(self.O)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpAdj) and self.O == other.O
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash(self.O)
    
class OpScal(DiracOp):
    def __init__(self, S: DiracScalar|TRSVar, O: DiracOp|TRSVar) :
        self.S = S
        self.O = O

    def __str__(self) -> str:
        return f"({self.S}.{self.O})"
    
    def __repr__(self) -> str:
        return f"({repr(self.S)} SCRO {repr(self.O)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpScal) and self.S == other.S and self.O == other.O
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.S, self.O))
    
class OpAdd(DiracOp, AC_symbol):
    PRINTING_INFIX = '+'
    EXPR_INFIX = 'ADDO'

    def __init__(self, tup : Tuple[DiracOp|TRSVar, ...]):
        AC_symbol.__init__(self, tup)

    def __str__(self) -> str:
        return AC_symbol.__str__(self)
    
    def __repr__(self) -> str:
        return AC_symbol.__repr__(self)
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpAdd) and self.tup == other.tup
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return AC_symbol.args_hash(self)
    
class OpApply(DiracOp):
    def __init__(self, O1: DiracOp|TRSVar, O2: DiracOp|TRSVar) :
        self.O1 = O1
        self.O2 = O2

    def __str__(self) -> str:
        return f"({self.O1} · {self.O2})"
    
    def __repr__(self) -> str:
        return f"({repr(self.O1)} MLTO {repr(self.O2)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpApply) and self.O1 == other.O1 and self.O2 == other.O2
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.O1, self.O2))
    
class OpTensor(DiracOp):
    def __init__(self, O1: DiracOp|TRSVar, O2: DiracOp|TRSVar) :
        self.O1 = O1
        self.O2 = O2

    def __str__(self) -> str:
        return f"({self.O1} ⊗ {self.O2})"
    
    def __repr__(self) -> str:
        return f"({repr(self.O1)} TSRO {repr(self.O2)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, OpTensor) and self.O1 == other.O1 and self.O2 == other.O2
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def args_hash(self) -> int:
        return hash((self.O1, self.O2))