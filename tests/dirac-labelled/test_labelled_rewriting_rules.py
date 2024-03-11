
from diracdec import *

from diracdec import parse, dirac_trs as trs, label_trs

def test_REG_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' FSTR(PAIRR(s, t)) ''')
        b = parse("s")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_REG_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SNDR(PAIRR(s, t)) ''')
        b = parse("t")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_REG_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' PAIRR(FSTR(s), SNDR(s)) ''')
        b = parse("s")
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_1():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S UNIONR ESETR ''')
        b = parse(r''' S ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_2():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S UNIONR S UNIONR S ''')
        b = parse(r''' S ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_3():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(FSTR(R)) UNIONR SETR(SNDR(R)) ''')
        b = parse(r''' R ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SETR(SNDR(R)) UNIONR SETR(FSTR(R)) UNIONR X ''')
        b = parse(r''' R UNIONR X''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_4():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SUBR ESETR ''')
        b = parse(r''' S0 ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_5():
    with wolfram_backend.wolfram_session():
        a = parse(r''' ESETR SUBR S0 ''')
        b = parse(r''' ESETR ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_6():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S0 SUBR S0 ''')
        b = parse(r''' ESETR ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_7():
    with wolfram_backend.wolfram_session():
        a = parse(r''' (S1 UNIONR S2) SUBR X ''')
        b = parse(r''' (S1 SUBR X) UNIONR (S2 SUBR X) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_8():
    with wolfram_backend.wolfram_session():
        a = parse(r''' S1 SUBR (S2 UNIONR S3) ''')
        b = parse(r''' (S1 SUBR S2) SUBR S3 ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_9():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(FSTR(R1)) UNIONR SETR(R1) ''')
        b = parse(r''' SETR(R1) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SETR(FSTR(PAIRR(R1, X))) UNIONR SETR(PAIRR(R1, R2)) ''')
        b = parse(r''' SETR(PAIRR(R1, R2)) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

        a = parse(r''' SETR(PAIRR(FSTR(R1), R2)) UNIONR SETR(PAIRR(R1, R2)) ''')
        b = parse(r''' SETR(PAIRR(R1, R2)) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)

def test_RSET_10():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(FSTR(R1)) SUBR SETR(R1) ''')
        b = parse(r''' ESETR ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_RSET_11():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(R1) SUBR SETR(FSTR(R1)) ''')
        b = parse(r''' (SETR(FSTR(R1)) SUBR SETR(FSTR(R1))) UNIONR (SETR(SNDR(R1)) SUBR SETR(FSTR(R1))) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)


def test_RSET_12():
    with wolfram_backend.wolfram_session():
        a = parse(r''' SETR(R1) SUBR SETR(R2) ''')
        b = parse(r''' SETR(R1) ''')
        assert label_trs.normalize(a) == label_trs.normalize(b)
