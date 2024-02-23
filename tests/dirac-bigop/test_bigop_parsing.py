from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_bigop_parse as parse

def test_scalar_sum():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUMS(x, x)''')
        b = ScalarSum(TRSVar("x"), TRSVar("x"))
        assert a == b

def test_abstraction():
    with wolfram_backend.wolfram_session():
        a = parse(r''' FUN x . x ''')
        b = Abstract(TRSVar("x"), TRSVar("x"))
        assert a == b

def test_apply():
    with wolfram_backend.wolfram_session():
        a = parse(r''' A @ B ''')
        b = Apply(TRSVar("A"), TRSVar("B"))
        assert a == b