'''
Defining the interfaces of a complex scalar system.
'''


from __future__ import annotations


from .trs import Term

from abc import abstractmethod

class ComplexScalar(Term):
    @staticmethod
    @abstractmethod
    def zero() -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def one() -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def conj(c : Term) -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def add(c1 : Term, c2 : Term) -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def mlt(c1 : Term, c2 : Term) -> ComplexScalar:
        pass


    @abstractmethod
    def reduce(self) -> ComplexScalar|None:
        '''
        reduce the expression, return the reduced result
        return None if it is already normal
        '''
        pass