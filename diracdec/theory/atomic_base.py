'''
The python script that defines the interface for an implementation of the atomic base
'''

from __future__ import annotations

from typing import Any

from .trs import TRSTerm, TRSSpec

from abc import abstractmethod

class AtomicBase(TRSSpec):
    '''
    The interface for an implementation of the atomic base
    '''

    @abstractmethod
    def eq_satisfiable(self, other) -> bool:
        '''
        check whether e1 == e2 is satisfiable with variables of [vars]
        '''
        pass
