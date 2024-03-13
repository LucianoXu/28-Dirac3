from diracdec import *
from diracdec.theory.dirac_bigop import *
from diracdec import parse, dirac_bigop_delta_trs as trs, juxt

def test_problem_1():
    '''
    Here is an unjoinable pair due to `DELTA(i, PAIR(s, s))`.
    '''
    with wolfram_backend.wolfram_session():
        a = parse(''' SUM(i, DELTA(i, PAIR(s, s)) SCR (KET(i) OUTER BRA(i))) ''')
        b = parse(''' KET(PAIR(s, s)) OUTER BRA(PAIR(s, s)) ''')
        assert trs.normalize(a) == trs.normalize(b)


def test_problem_2():
    '''
    sum elimination is not complete. these two terms can be not joinable when X is pushed inside the sum first.
    '''
    with wolfram_backend.wolfram_session():
        a = parse('''X TSR SUM(i, (BRA(i) DOT K0) SCR KET(i))''')
        b = parse('''X TSR K0''')
        assert entry_trs.normalize(trs.normalize(a)) == entry_trs.normalize(trs.normalize(b))
