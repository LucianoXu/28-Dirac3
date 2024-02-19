
from diracdec import *


def test_1():
    with wolfram_backend.wolfram_session():
        a = ScalarAdd(TRSVar('A'), TRSVar('B'), TRSVar('A'))
        b = ScalarAdd(TRSVar('A'), TRSVar('A'), TRSVar('B'))
        assert a == b
        assert hash(a) == hash(b)


def test_2():
    with wolfram_backend.wolfram_session():
        a = ScalarAdd(TRSVar('A'), TRSVar('A'), TRSVar('B'))
        b = ScalarMlt(TRSVar('A'), TRSVar('A'), TRSVar('B'))
        assert a != b
        assert hash(a) != hash(b)   # this should hold with very high probability


