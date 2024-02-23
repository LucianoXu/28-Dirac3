'''
The python script that defines the interface for an implementation of the atomic base
'''

from __future__ import annotations

from typing import Any

from .trs import TRSTerm

from abc import abstractmethod

class AtomicBase(TRSTerm):
    '''
    The interface for an implementation of the atomic base
    '''

    @abstractmethod
    def eq_satisfiable(self, other) -> bool:
        '''
        check whether e1 == e2 is satisfiable with variables of [vars]
        '''
        pass

    @abstractmethod
    def reduce(self) -> AtomicBase|None:
        '''
        reduce the expression, return the reduced result
        return None if it is already normal
        '''
        pass
