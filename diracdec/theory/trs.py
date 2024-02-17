'''
The architecture of the term rewriting system
'''

from __future__ import annotations

from abc import ABC, abstractmethod


class TRSTerm(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other: TRSTerm) -> bool:
        '''
        This method calculates the equivalence in pure syntactic level.
        '''
        pass

    @abstractmethod
    def args_hash(self) -> int:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        return hash((type(self).__name__, self.args_hash()))

class TRSVar(TRSTerm):

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, other: TRSVar) -> bool:
        return isinstance(other, TRSVar) and self.name == other.name
    
    def __hash__(self) -> int:
        return super().__hash__()

    def args_hash(self) -> int:
        return hash(self.name)   