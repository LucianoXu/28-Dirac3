from diracdec import *

from diracdec import dirac_parse as parse, dirac_trs as trs


# these tests are based on wolfram engine for complex and basis
def test_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''CONJS("0" ADDS "0" ADDS CONJS(CONJS("0"))) ADDS "0"''')
        b = parse(r'''CONJS("0")''')

        assert trs.normalize(a) == trs.normalize(b)



