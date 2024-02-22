'''
Defining the interfaces of a complex scalar system.
'''


from __future__ import annotations


from .trs import TRSTerm, TRSSpec

from abc import abstractmethod

class ComplexScalar(TRSSpec):
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
    def conj(c : TRSTerm) -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def add(c1 : TRSTerm, c2 : TRSTerm) -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def mlt(c1 : TRSTerm, c2 : TRSTerm) -> ComplexScalar:
        pass