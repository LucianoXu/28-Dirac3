'''
The python script that defines the interface for an implementation of the atomic base
'''

from __future__ import annotations

from typing import Any

from abc import ABC, abstractmethod

class AtomicBase(ABC):
    '''
    The interface for an implementation of the atomic base
    '''
    @abstractmethod
    def __str__(self) -> str:
        '''
        Returns a string representation of the atomic base
        '''
        pass

    @abstractmethod
    def __repr__(self) -> str:
        '''
        Returns a string representation of the atomic base
        '''
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        '''
        Returns True if the atomic base is equal to the other atomic base
        '''
        pass

    @abstractmethod
    def __hash__(self) -> int:
        '''
        Returns the hash of the atomic base
        '''
        pass