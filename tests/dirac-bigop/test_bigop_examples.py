from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_bigop_parse as parse

def test_1():
    with wolfram_backend.wolfram_session():
        a = parse(''' SUMS(a, "a")''')
        sub = Subst({
            "a" : parse(''' "1" '''),
        })
        assert a == sub(a)
        assert hash(a) == hash(sub(a))