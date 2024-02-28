from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import dirac_bigop_delta_parse as parse, dirac_bigop_delta_trs as trs, juxt, sumeq

def test_problem_1():
    '''
    Here is an unjoinable pair due to `DELTA(i, PAIR(s, s))`.
    '''
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, DELTA(i, PAIR(s, s)) SCRO (KET(i) OUTER BRA(i))) ''')
        b = parse(''' KET(PAIR(s, s)) OUTER BRA(PAIR(s, s)) ''')
        assert trs.normalize(a) == trs.normalize(b)