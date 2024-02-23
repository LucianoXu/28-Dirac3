from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_bigop_parse as parse

def test_scalar_sum():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SUMS(x, x)''')
        b = ScalarSum(TRSVar("x"), TRSVar("x"))
        assert a == b
