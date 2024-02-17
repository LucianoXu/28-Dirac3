
from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Tuple, List, Type

from .atomic_base import AtomicBase
from .complex_scalar import ComplexScalar

from .trs import TRSTerm, TRSVar



################################################################
# techniques for AC-symbols


class AC_symbol:
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
        return f"BaseAtom({self.b})"
    
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
        return f"BasePair({self.left}, {self.right})"
    
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
        return f"fst({self.p})"
    
    def __repr__(self) -> str:
        return f"BaseFst({self.p})"
    
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
        return f"snd({self.p})"
    
    def __repr__(self) -> str:
        return f"BaseSnd({self.p})"
    
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
        return f'C("{self.c}")'
    
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
        return f"ScalarDelta({self.b1}, {self.b2})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarDelta) and self.b1 == other.b1 and self.b2 == other.b2
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash((self.b1, self.b2))


class ScalarAdd(DiracScalar, AC_symbol):
    def __init__(self, tup : Tuple[DiracScalar | TRSVar, ...]):
        AC_symbol.__init__(self, tup)

    def __str__(self) -> str:
        res = f"({self.tup[0]}"

        for item in self.tup[1:]:
            res += f" + {item}"

        return res + ")"
    
    def __repr__(self) -> str:
        return f"ScalarAdd({repr(self.tup)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarAdd) and self.tup == other.tup
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(tuple([hash(item) for item in self.tup]))
    
class ScalarMlt(DiracScalar, AC_symbol):
    def __init__(self, tup : Tuple[DiracScalar | TRSVar, ...]):
        AC_symbol.__init__(self, tup)

    def __str__(self) -> str:
        res = f"({self.tup[0]}"

        for item in self.tup[1:]:
            res += f" × {item}"

        return res + ")"
    
    def __repr__(self) -> str:
        return f"ScalarMlt({repr(self.tup)})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarMlt) and self.tup == other.tup
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(tuple([hash(item) for item in self.tup]))
    
class ScalarConj(DiracScalar):
    def __init__(self, s : DiracScalar | TRSVar):
        self.s = s

    def __str__(self) -> str:
        return f"({self.s})^*"
    
    def __repr__(self) -> str:
        return f"ScalarConj({self.s})"
    
    def __eq__(self, other: TRSTerm) -> bool:
        return isinstance(other, ScalarConj) and self.s == other.s
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.s)

############################################
# DiracKet
    