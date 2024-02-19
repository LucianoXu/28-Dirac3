

from diracdec import *


def test_1():
    with wolfram_backend.wolfram_session():
        a = parse(r'''CONJS("0" ADDS "0" ADDS CONJS(CONJS("0"))) ADDS "0"''')
        b = parse(r'''CONJS("0")''')

        assert diractrs.normalize(a) == diractrs.normalize(b)

