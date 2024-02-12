'''
Defining the interfaces of a complex scalar system.
'''


from __future__ import annotations

from typing import Any

from abc import ABC, abstractmethod

class ComplexScalar(ABC):
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
    def conj(c : ComplexScalar) -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def add(c1 : ComplexScalar, c2 : ComplexScalar) -> ComplexScalar:
        pass

    @staticmethod
    @abstractmethod
    def mlt(c1 : ComplexScalar, c2 : ComplexScalar) -> ComplexScalar:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other: ComplexScalar) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass