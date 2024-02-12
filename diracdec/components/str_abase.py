'''
The implementation for complex scalar system by python floating point numbers
'''

from __future__ import annotations

from ..theory.atomic_base import AtomicBase


class StrABase(AtomicBase):
    def __init__(self, s : str):
        self.s = s

    def __str__(self) -> str:
        return self.s
    
    def __repr__(self) -> str:
        return f'StrABase({self.s})"'
    
    def __eq__(self, other: StrABase) -> bool:
        return isinstance(other, StrABase) and self.s == other.s
    
    def __hash__(self) -> int:
        return hash(self.s)