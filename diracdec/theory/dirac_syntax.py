
from __future__ import annotations
from abc import ABC, abstractmethod

from .atomic_base import AtomicBase
from .complex_scalar import ComplexScalar

from .trs import TRSTerm, TRSVar



class DiracSyntax(TRSTerm):
    def __hash__(self) -> int:
        return super().__hash__()


# DiracBase

class DiracBase(DiracSyntax):
    def __hash__(self) -> int:
        return super().__hash__()
    
    
class DiracBaseAtom(DiracBase):

    def __init__(self, b : AtomicBase | TRSVar):
        '''
        b is the atomic base
        '''
        self.b = b
    
    def __str__(self) -> str:
        return f"'{str(self.b)}'"
    
    def __repr__(self) -> str:
        return f"BaseAtom({self.b})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, DiracBaseAtom) and self.b == other.b
    
    def __hash__(self) -> int:
        return super().__hash__()

    
    def args_hash(self) -> int:
        return hash(self.b)
    
    
class DiracBasePair(DiracBase):
    
    def __init__(self, left: DiracBase | TRSVar, right: DiracBase | TRSVar):
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        return f"({self.left}, {self.right})"
    
    def __repr__(self) -> str:
        return f"BasePair({self.left}, {self.right})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, DiracBasePair) and self.left == other.left and self.right == other.right
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash((self.left, self.right))
    
class DiracBaseFst(DiracBase):
    def __init__(self, p: DiracBasePair | TRSVar):
        self.p = p

    def __str__(self) -> str:
        return f"fst({self.p})"
    
    def __repr__(self) -> str:
        return f"BaseFst({self.p})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, DiracBaseFst) and self.p == other.p
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.p)
    
class DiracBaseSnd(DiracBase):
    def __init__(self, p: DiracBasePair | TRSVar):
        self.p = p

    def __str__(self) -> str:
        return f"snd({self.p})"
    
    def __repr__(self) -> str:
        return f"BaseSnd({self.p})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, DiracBaseSnd) and self.p == other.p
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.p)
    

# DiracScalar
class DiracScalar(DiracSyntax):
    def __hash__(self) -> int:
        return super().__hash__()


class DiracScalarC(DiracScalar):
    def __init__(self, c : ComplexScalar):
        self.c = c

    def __str__(self) -> str:
        return f'"{self.c}"'
    
    def __repr__(self) -> str:
        return f'C("{self.c}")'
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, DiracScalarC) and self.c == other.c
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.c)

class DiracScalarDelta(DiracScalar):
    def __init__(self, b1 : AtomicBase | TRSVar, b2 : AtomicBase | TRSVar):
        self.b1 = b1
        self.b2 = b2

    def __str__(self) -> str:
        return f"δ({self.b1}, {self.b2})"
    
    def __repr__(self) -> str:
        return f"ScalarDelta({self.b1}, {self.b2})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, DiracScalarDelta) and self.b1 == other.b1 and self.b2 == other.b2
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash((self.b1, self.b2))