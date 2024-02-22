

from diracdec import *

from diracdec import dirac_delta_parse as parse, dirac_delta_trs as trs


def test_DELTA_AST_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA(s, s) ''')
        b = parse(r''' "1" ''')
        assert trs.normalize(a) == trs.normalize(b)

        a = parse(r''' DELTA('1', '0.5+0.5') ''')
        b = parse(r''' "1" ''')
        assert trs.normalize(a) == trs.normalize(b)

def test_DELTA_AST_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' DELTA('0', '1') ''')
        b = parse(r''' "0" ''')
        print(trs.normalize(a))
        print(trs.normalize(b))
        
        a = parse(r''' DELTA('x', 'x+1') ''')
        b = parse(r''' "0" ''')
        print(trs.normalize(a))
        print(trs.normalize(b))
