'''
The implementation for complex scalar system by python floating point numbers
'''

from __future__ import annotations

from ..theory.complex_scalar import ComplexScalar

class PyCScalar(ComplexScalar):
    def __init__(self, c : complex | str):
        if isinstance(c, str):
            c = complex(c)
        self.c = c

    @staticmethod
    def zero() -> PyCScalar:
        return PyCScalar(0)
    
    @staticmethod
    def one() -> PyCScalar:
        return PyCScalar(1)
    
    @staticmethod
    def conj(c : PyCScalar) -> PyCScalar:
        return PyCScalar(c.c.conjugate())
    
    @staticmethod
    def add(c1 : PyCScalar, c2 : PyCScalar) -> PyCScalar:
        return PyCScalar(c1.c + c2.c)
    
    @staticmethod
    def mlt(c1 : PyCScalar, c2 : PyCScalar) -> PyCScalar:
        return PyCScalar(c1.c * c2.c)
    
    def __str__(self) -> str:
        return f'{str(self.c)}'
    
    def __repr__(self) -> str:
        return f'PyCScalar({self.c})'
    
    def __eq__(self, other: PyCScalar) -> bool:
        return isinstance(other, PyCScalar) and self.c == other.c
    
    def __hash__(self) -> int:
        return hash(self.c)